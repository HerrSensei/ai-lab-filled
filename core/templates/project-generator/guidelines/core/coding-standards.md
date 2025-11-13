# AI-LAB Coding Standards

## Core Principles

1. **Clarity First** - Code should be self-documenting
2. **Consistency** - Follow established patterns across all projects
3. **Security** - Security is a requirement, not an afterthought
4. **Performance** - Write efficient, scalable code
5. **Maintainability** - Future developers should understand your code

## Python Standards

### Code Style
- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Imports**: isort for organization, standard library first

### Documentation
- **Docstrings**: Google style for all functions and classes
- **Type Hints**: Required for all function parameters and returns
- **Comments**: Explain "why", not "what"

### Code Quality
- **Linting**: flake8 with strict configuration
- **Formatting**: black for consistent style
- **Testing**: pytest with 80% minimum coverage

## JavaScript/TypeScript Standards

### Code Style
- **Line Length**: 100 characters
- **Indentation**: 2 spaces
- **Naming**: camelCase for variables/functions, PascalCase for classes
- **Semicolons**: Required

### Documentation
- **JSDoc**: Required for all public functions
- **TypeScript**: Strong typing preferred
- **Comments**: Explain complex logic

## Security Standards

### Input Validation
- **Never trust user input**
- **Validate all inputs at entry points**
- **Sanitize data for output context**

### Authentication & Authorization
- **Use established libraries**
- **Implement rate limiting**
- **Secure password handling (bcrypt)**

### Data Protection
- **Encrypt sensitive data at rest**
- **Use HTTPS in production**
- **Implement proper logging (no sensitive data)**

## Testing Standards

### Test Types
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Coverage Requirements
- **Minimum 80% line coverage**
- **Critical paths 100% covered**
- **All edge cases tested**

## Git Standards

### Commit Messages
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, test, chore
- **Examples**:
  - `feat(api): add user authentication`
  - `fix(ui): resolve login button issue`

### Branch Strategy
- **main**: Production-ready code
- **develop**: Integration branch
- **feature/***: New features
- **hotfix/***: Critical fixes

## Documentation Standards

### README Requirements
- **Project description**
- **Installation instructions**
- **Usage examples**
- **API documentation**
- **Contributing guidelines**

### Code Documentation
- **API docs**: Auto-generated from docstrings
- **Architecture docs**: High-level system design
- **Deployment docs**: Environment setup

## Performance Standards

### Response Times
- **API responses**: < 200ms for 95th percentile
- **Page loads**: < 3 seconds
- **Database queries**: Optimized with proper indexes

### Resource Usage
- **Memory**: Monitor for leaks
- **CPU**: Profile bottlenecks
- **Network**: Minimize payload sizes

## Monitoring & Logging

### Logging Levels
- **ERROR**: System failures
- **WARN**: Deprecated features, performance issues
- **INFO**: Important events
- **DEBUG**: Detailed troubleshooting

### Metrics
- **Performance**: Response times, throughput
- **Business**: User actions, conversions
- **System**: Resource usage, error rates

## Review Checklist

### Before Commit
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Security review completed
- [ ] Performance impact assessed

### Before Release
- [ ] Full test suite passes
- [ ] Security scan completed
- [ ] Performance tests pass
- [ ] Documentation complete
- [ ] Rollback plan prepared
