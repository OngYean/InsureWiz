/**
 * Vehicle data caching service for frontend-side filtering
 * Provides lightning-fast suggestions by caching year data locally
 */

export interface YearData {
  brands: string[]
  models: Record<string, string[]>
  colors: Record<string, Record<string, string[]>>
}

export interface SuggestionResult {
  primary: string | null
  suggestions: string[]
  completion: string
}

class VehicleCacheService {
  private cache: Map<number, YearData> = new Map()
  private readonly CACHE_DURATION = 24 * 60 * 60 * 1000 // 24 hours
  private readonly CACHE_KEY_PREFIX = 'vehicle-data-'
  
  constructor(private apiBase: string) {
    this.loadFromLocalStorage()
  }

  /**
   * Get year data with caching
   */
  async getYearData(year: number): Promise<YearData> {
    // Check memory cache first
    if (this.cache.has(year)) {
      return this.cache.get(year)!
    }

    // Check localStorage cache
    const cached = this.getFromLocalStorage(year)
    if (cached) {
      this.cache.set(year, cached)
      return cached
    }

    // Fetch from API
    try {
      const response = await fetch(`${this.apiBase}/api/validator/year-data/${year}`)
      if (!response.ok) {
        throw new Error(`Failed to fetch year data: ${response.statusText}`)
      }
      
      const data: YearData = await response.json()
      
      // Cache in memory and localStorage
      this.cache.set(year, data)
      this.saveToLocalStorage(year, data)
      
      return data
    } catch (error) {
      console.error('Error fetching year data:', error)
      throw error
    }
  }

  /**
   * Get brand suggestions with fuzzy matching
   */
  getBrandSuggestions(year: number, query: string): SuggestionResult {
    const yearData = this.cache.get(year)
    if (!yearData) {
      return { primary: null, suggestions: [], completion: '' }
    }

    if (!query.trim()) {
      return {
        primary: null,
        suggestions: yearData.brands.slice(0, 5),
        completion: ''
      }
    }

    const matches = this.fuzzyMatch(query, yearData.brands)
    return this.formatSuggestionResult(query, matches)
  }

  /**
   * Get model suggestions for a specific brand
   */
  getModelSuggestions(year: number, brand: string, query: string): SuggestionResult {
    const yearData = this.cache.get(year)
    if (!yearData || !yearData.models[brand]) {
      return { primary: null, suggestions: [], completion: '' }
    }

    const models = yearData.models[brand]
    
    if (!query.trim()) {
      return {
        primary: null,
        suggestions: models.slice(0, 5),
        completion: ''
      }
    }

    const matches = this.fuzzyMatch(query, models)
    return this.formatSuggestionResult(query, matches)
  }

  /**
   * Get color suggestions for a specific brand and model
   */
  getColorSuggestions(year: number, brand: string, model: string, query: string): SuggestionResult {
    const yearData = this.cache.get(year)
    if (!yearData || !yearData.colors[brand]?.[model]) {
      return { primary: null, suggestions: [], completion: '' }
    }

    const colors = yearData.colors[brand][model]
    
    if (!query.trim()) {
      return {
        primary: null,
        suggestions: colors.slice(0, 5),
        completion: ''
      }
    }

    const matches = this.fuzzyMatch(query, colors)
    return this.formatSuggestionResult(query, matches)
  }

  /**
   * Preload data for multiple years (background loading)
   */
  async preloadYears(years: number[]): Promise<void> {
    const promises = years.map(year => 
      this.getYearData(year).catch(error => {
        console.warn(`Failed to preload year ${year}:`, error)
        return null
      })
    )
    
    await Promise.allSettled(promises)
  }

  /**
   * Clear cache for a specific year or all years
   */
  clearCache(year?: number): void {
    if (year !== undefined) {
      this.cache.delete(year)
      localStorage.removeItem(`${this.CACHE_KEY_PREFIX}${year}`)
    } else {
      this.cache.clear()
      // Clear all vehicle data from localStorage
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const key = localStorage.key(i)
        if (key?.startsWith(this.CACHE_KEY_PREFIX)) {
          localStorage.removeItem(key)
        }
      }
    }
  }

  /**
   * Check if year data is cached
   */
  isYearCached(year: number): boolean {
    return this.cache.has(year) || this.hasValidLocalStorageCache(year)
  }

  /**
   * Fuzzy matching algorithm with scoring
   */
  private fuzzyMatch(query: string, candidates: string[]): Array<{text: string, score: number}> {
    const queryLower = query.toLowerCase().trim()
    
    if (!queryLower) return []

    const matches = candidates.map(candidate => {
      const candidateLower = candidate.toLowerCase()
      let score = 0

      // Exact match (highest score)
      if (candidateLower === queryLower) {
        score = 1.0
      }
      // Starts with query (high score)
      else if (candidateLower.startsWith(queryLower)) {
        score = 0.9
      }
      // Contains query (medium score)
      else if (candidateLower.includes(queryLower)) {
        score = 0.7
      }
      // Character similarity (lower score)
      else {
        score = this.calculateSimilarity(queryLower, candidateLower)
      }

      return { text: candidate, score }
    })

    // Filter and sort by score
    return matches
      .filter(match => match.score >= 0.3)
      .sort((a, b) => b.score - a.score)
      .slice(0, 10)
  }

  /**
   * Calculate string similarity using Jaro-Winkler-like algorithm
   */
  private calculateSimilarity(a: string, b: string): number {
    if (a === b) return 1.0
    if (a.length === 0 || b.length === 0) return 0.0

    const matchDistance = Math.floor(Math.max(a.length, b.length) / 2) - 1
    const aMatches = new Array(a.length).fill(false)
    const bMatches = new Array(b.length).fill(false)

    let matches = 0
    let transpositions = 0

    // Find matches
    for (let i = 0; i < a.length; i++) {
      const start = Math.max(0, i - matchDistance)
      const end = Math.min(i + matchDistance + 1, b.length)

      for (let j = start; j < end; j++) {
        if (bMatches[j] || a[i] !== b[j]) continue
        aMatches[i] = bMatches[j] = true
        matches++
        break
      }
    }

    if (matches === 0) return 0.0

    // Find transpositions
    let k = 0
    for (let i = 0; i < a.length; i++) {
      if (!aMatches[i]) continue
      while (!bMatches[k]) k++
      if (a[i] !== b[k]) transpositions++
      k++
    }

    return (matches / a.length + matches / b.length + (matches - transpositions / 2) / matches) / 3
  }

  /**
   * Format suggestion result with completion text
   */
  private formatSuggestionResult(query: string, matches: Array<{text: string, score: number}>): SuggestionResult {
    if (matches.length === 0) {
      return { primary: null, suggestions: [], completion: '' }
    }

    const primary = matches[0]
    const completion = this.getCompletion(query, primary.text)

    return {
      primary: primary.text,
      suggestions: matches.map(m => m.text),
      completion
    }
  }

  /**
   * Get tab completion text
   */
  private getCompletion(query: string, match: string): string {
    const queryLower = query.toLowerCase()
    const matchLower = match.toLowerCase()

    if (matchLower.startsWith(queryLower)) {
      return match.slice(query.length)
    }
    return ''
  }

  /**
   * Load cache from localStorage on initialization
   */
  private loadFromLocalStorage(): void {
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)
        if (key?.startsWith(this.CACHE_KEY_PREFIX)) {
          const year = parseInt(key.replace(this.CACHE_KEY_PREFIX, ''))
          const data = this.getFromLocalStorage(year)
          if (data) {
            this.cache.set(year, data)
          }
        }
      }
    } catch (error) {
      console.warn('Error loading cache from localStorage:', error)
    }
  }

  /**
   * Get data from localStorage with expiration check
   */
  private getFromLocalStorage(year: number): YearData | null {
    try {
      const item = localStorage.getItem(`${this.CACHE_KEY_PREFIX}${year}`)
      if (!item) return null

      const { data, timestamp } = JSON.parse(item)
      
      // Check if cache is still valid
      if (Date.now() - timestamp > this.CACHE_DURATION) {
        localStorage.removeItem(`${this.CACHE_KEY_PREFIX}${year}`)
        return null
      }

      return data
    } catch (error) {
      console.warn(`Error reading cache for year ${year}:`, error)
      return null
    }
  }

  /**
   * Save data to localStorage with timestamp
   */
  private saveToLocalStorage(year: number, data: YearData): void {
    try {
      const item = {
        data,
        timestamp: Date.now()
      }
      localStorage.setItem(`${this.CACHE_KEY_PREFIX}${year}`, JSON.stringify(item))
    } catch (error) {
      console.warn(`Error saving cache for year ${year}:`, error)
    }
  }

  /**
   * Check if localStorage cache is valid
   */
  private hasValidLocalStorageCache(year: number): boolean {
    return this.getFromLocalStorage(year) !== null
  }
}

// Export singleton instance
export const vehicleCache = new VehicleCacheService(
  process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
)
