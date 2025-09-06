# InsureWiz Documentation Index

## Overview
This document provides a comprehensive index of all InsureWiz project documentation, organized for easy navigation and reference. This documentation is designed to support RAG (Retrieval-Augmented Generation) systems and provide comprehensive information about the Malaysian insurance and Takaful platform.

## Documentation Structure

### 1. Project Overview Documents

#### [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- **Purpose**: High-level project description and business value
- **Content**: Project description, core purpose, key features, target users, business value, technology stack, architecture pattern
- **Use Case**: Understanding what InsureWiz is and why it exists
- **RAG Relevance**: Provides context for AI systems to understand the project's purpose and scope

#### [README.md](./README.md)
- **Purpose**: Main project documentation with setup instructions
- **Content**: Features, architecture, prerequisites, quick start, configuration, API docs, usage, development, deployment
- **Use Case**: Getting started with the project and understanding its capabilities
- **RAG Relevance**: Comprehensive project overview with practical implementation details

### 2. Technical Architecture Documents

#### [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)
- **Purpose**: Detailed technical implementation and system design
- **Content**: System architecture, backend/frontend structure, data flow, security, performance, scalability, monitoring
- **Use Case**: Understanding how the system is built and how components interact
- **RAG Relevance**: Technical details for developers and system architects

#### [API_REFERENCE.md](./API_REFERENCE.md)
- **Purpose**: Complete API documentation with examples
- **Content**: All endpoints, request/response formats, status codes, error handling, authentication, rate limiting
- **Use Case**: Integrating with the InsureWiz API or understanding available functionality
- **RAG Relevance**: API specifications for integration and development

### 3. Development and Implementation Documents

#### [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)
- **Purpose**: Comprehensive development setup and workflow
- **Content**: Environment setup, project structure, development workflow, code standards, testing, debugging, deployment
- **Use Case**: Setting up development environment and contributing to the project
- **RAG Relevance**: Development practices and coding standards

#### [AI_INTEGRATION_GUIDE.md](./AI_INTEGRATION_GUIDE.md)
- **Purpose**: AI features implementation and configuration
- **Content**: AI architecture, Google Gemini integration, LangChain setup, conversation management, performance optimization
- **Use Case**: Understanding and extending AI capabilities
- **RAG Relevance**: Core AI implementation details and best practices

### 4. Backend-Specific Documentation

#### [backend/README.md](./backend/README.md)
- **Purpose**: Backend-specific setup and configuration
- **Content**: Python environment, dependencies, configuration, startup
- **Use Case**: Setting up and running the backend server
- **RAG Relevance**: Backend implementation details

#### [backend/PROJECT_STRUCTURE.md](./backend/PROJECT_STRUCTURE.md)
- **Purpose**: Backend code organization and structure
- **Content**: Directory layout, module organization, file purposes
- **Use Case**: Understanding backend codebase organization
- **RAG Relevance**: Code structure and organization patterns

### 5. Frontend-Specific Documentation

#### [frontend/package.json](./frontend/package.json)
- **Purpose**: Frontend dependencies and scripts
- **Content**: Node.js dependencies, build scripts, project metadata
- **Use Case**: Understanding frontend technology stack and build process
- **RAG Relevance**: Frontend technology choices and dependencies

## Quick Reference Guide

### For Developers
1. **Start Here**: [README.md](./README.md) - Complete project overview
2. **Setup Development**: [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md) - Environment setup
3. **Understand Architecture**: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md) - System design
4. **API Integration**: [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
5. **AI Features**: [AI_INTEGRATION_GUIDE.md](./AI_INTEGRATION_GUIDE.md) - AI implementation

### For RAG Systems
1. **Project Context**: [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - High-level understanding
2. **Technical Details**: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md) - Implementation specifics
3. **API Information**: [API_REFERENCE.md](./API_REFERENCE.md) - Integration details
4. **AI Capabilities**: [AI_INTEGRATION_GUIDE.md](./AI_INTEGRATION_GUIDE.md) - AI feature details

### For Business Users
1. **Project Overview**: [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - Business value and purpose
2. **Features**: [README.md](./README.md) - Available functionality
3. **Architecture**: [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md) - System capabilities

## Document Categories

### Business Documentation
- **Purpose**: Understanding project value and business context
- **Documents**: PROJECT_OVERVIEW.md, README.md
- **Audience**: Stakeholders, product managers, business analysts

### Technical Documentation
- **Purpose**: Implementation details and technical specifications
- **Documents**: TECHNICAL_ARCHITECTURE.md, API_REFERENCE.md, AI_INTEGRATION_GUIDE.md
- **Audience**: Developers, architects, DevOps engineers

### Development Documentation
- **Purpose**: Setting up and contributing to the project
- **Documents**: DEVELOPMENT_GUIDE.md, backend/README.md, frontend/package.json
- **Audience**: Developers, contributors, maintainers

## Key Information by Topic

### Malaysian Insurance & Takaful Domain Knowledge
- **Location**: PROJECT_OVERVIEW.md, AI_INTEGRATION_GUIDE.md
- **Content**: Malaysian insurance concepts, Takaful principles, policy types, claims processing, vehicle validation, JPJ integration, NCD system, panel hospitals
- **RAG Use**: Understanding Malaysian insurance terminology, Takaful principles, and local market processes

### Technology Stack
- **Location**: TECHNICAL_ARCHITECTURE.md, README.md
- **Content**: FastAPI, Next.js, LangChain, Google Gemini, Tailwind CSS
- **RAG Use**: Understanding technical capabilities and limitations

### API Endpoints
- **Location**: API_REFERENCE.md
- **Content**: Chat, policies, claims, vehicles, health check
- **RAG Use**: Understanding available functionality and integration points

### AI Integration
- **Location**: AI_INTEGRATION_GUIDE.md
- **Content**: LangChain setup, conversation management, prompt engineering, Malaysian insurance expertise, multi-language support
- **RAG Use**: Understanding AI capabilities, Malaysian insurance knowledge, and implementation patterns

### Development Process
- **Location**: DEVELOPMENT_GUIDE.md
- **Content**: Setup, coding standards, testing, deployment
- **RAG Use**: Understanding development practices and contribution guidelines

## Document Maintenance

### Update Frequency
- **High Priority**: README.md, API_REFERENCE.md - Update with each release
- **Medium Priority**: TECHNICAL_ARCHITECTURE.md, DEVELOPMENT_GUIDE.md - Update with major changes
- **Low Priority**: PROJECT_OVERVIEW.md - Update with project evolution

### Contributing to Documentation
1. Follow the same process as code contributions
2. Update relevant documentation when adding features
3. Ensure documentation accuracy and completeness
4. Use clear, concise language and examples

### Documentation Standards
- Use Markdown format for consistency
- Include code examples where appropriate
- Provide clear navigation and structure
- Keep content up-to-date with code changes

## RAG System Integration

### Document Embedding
- **Recommended**: Use semantic search for finding relevant documentation
- **Structure**: Organize by topic and purpose for better retrieval
- **Metadata**: Include tags and categories for improved search

### Context Window Management
- **Strategy**: Break large documents into logical sections
- **Chunking**: Use headers and sections for natural document boundaries
- **Cross-references**: Link related documents for comprehensive understanding

### Version Control
- **Tracking**: Document changes alongside code changes
- **Consistency**: Ensure documentation reflects current implementation
- **History**: Maintain change logs for major updates

## Support and Resources

### Getting Help
1. **Documentation Issues**: Check for updates and corrections
2. **Technical Questions**: Review relevant technical documents
3. **Development Issues**: Follow troubleshooting guides in DEVELOPMENT_GUIDE.md
4. **AI Integration**: Refer to AI_INTEGRATION_GUIDE.md for AI-specific issues

### Additional Resources
- **GitHub Repository**: Source code and issue tracking
- **API Documentation**: Interactive docs at `/docs` endpoint
- **Community**: Discussions and contributions welcome

---

*This documentation index is maintained alongside the InsureWiz project. For the most up-to-date information, always refer to the latest version of each document.*
