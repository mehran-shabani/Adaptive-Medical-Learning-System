# Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Configuration ⚠️ CRITICAL

- [ ] Copy `.env.example` to `.env`
- [ ] Set `JWT_SECRET_KEY` to a secure random value (min 32 characters)
- [ ] Configure `DATABASE_URL` with production database credentials
- [ ] Add `OPENAI_API_KEY` for AI features
- [ ] Set `REDIS_URL` for background tasks
- [ ] Update `ENVIRONMENT` to `production`
- [ ] Set `DEBUG=false`
- [ ] Configure `MAX_UPLOAD_SIZE_MB` appropriately

### 2. Database Setup

- [ ] Install PostgreSQL 14 or higher
- [ ] Install pgvector extension: `CREATE EXTENSION vector;`
- [ ] Create database: `createdb adaptive_medical_learning`
- [ ] Test connection with credentials in `.env`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Verify all tables created successfully

### 3. Dependencies

- [ ] Python 3.11 or higher installed
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify installations: `pip list`

### 4. Redis Setup

- [ ] Install Redis 7 or higher
- [ ] Start Redis service
- [ ] Test connection: `redis-cli ping`
- [ ] Configure persistence if needed

### 5. Security Review

- [ ] JWT_SECRET_KEY is unique and secure
- [ ] Database passwords are strong
- [ ] API keys are not hardcoded
- [ ] CORS origins configured for your domain
- [ ] File upload limits set appropriately
- [ ] Rate limiting configured (if needed)

### 6. File System

- [ ] Create uploads directory: `mkdir -p uploads`
- [ ] Set proper permissions: `chmod 755 uploads`
- [ ] Configure backup for uploads directory
- [ ] Consider using S3/MinIO for production

### 7. Testing

- [ ] Run syntax check: `python -m py_compile app/**/*.py`
- [ ] Test health endpoint: `curl http://localhost:8000/health`
- [ ] Test OTP flow
- [ ] Upload a test PDF
- [ ] Generate test quiz questions
- [ ] Get test study plan
- [ ] Check all API documentation at `/docs`

### 8. Monitoring & Logging

- [ ] Configure structured logging
- [ ] Set up log aggregation (e.g., ELK, Datadog)
- [ ] Configure error tracking (e.g., Sentry)
- [ ] Set up uptime monitoring
- [ ] Configure alerting for critical errors

### 9. Performance

- [ ] Test with expected load
- [ ] Optimize database queries if needed
- [ ] Configure connection pooling
- [ ] Set up caching strategy
- [ ] Monitor memory usage
- [ ] Profile slow endpoints

### 10. Backup Strategy

- [ ] Database backup schedule configured
- [ ] Test database restore procedure
- [ ] Backup uploaded files
- [ ] Document recovery procedures
- [ ] Store backups in separate location

## Docker Deployment Checklist

### 1. Docker Setup

- [ ] Docker and Docker Compose installed
- [ ] Build image: `docker-compose build`
- [ ] Test locally: `docker-compose up`
- [ ] Check all containers running: `docker-compose ps`

### 2. Production Configuration

- [ ] Update `docker-compose.yml` for production
- [ ] Remove port mappings for internal services
- [ ] Configure restart policies: `restart: always`
- [ ] Set resource limits (CPU, memory)
- [ ] Configure health checks

### 3. Networking

- [ ] Configure reverse proxy (nginx/traefik)
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up load balancer if needed

### 4. Volumes

- [ ] Configure persistent volumes
- [ ] Database data persistence
- [ ] Redis data persistence
- [ ] Uploads directory persistence
- [ ] Test volume backups

## Post-Deployment Checklist

### 1. Verification

- [ ] All services running
- [ ] Health check passing
- [ ] API accessible via HTTPS
- [ ] Database queries working
- [ ] Background tasks processing
- [ ] File uploads working

### 2. Initial Data

- [ ] Create admin user
- [ ] Load initial topics
- [ ] Upload sample content (optional)
- [ ] Test complete user flow

### 3. Documentation

- [ ] Document API endpoints
- [ ] Create user guide
- [ ] Document admin procedures
- [ ] Update deployment guide
- [ ] Document troubleshooting steps

### 4. Monitoring

- [ ] Verify monitoring is working
- [ ] Test alerting
- [ ] Review initial metrics
- [ ] Set baseline performance metrics

### 5. Security Scan

- [ ] Run security audit
- [ ] Check for exposed secrets
- [ ] Verify SSL configuration
- [ ] Test authentication flow
- [ ] Review access logs

## Maintenance Checklist

### Daily

- [ ] Check error logs
- [ ] Monitor API response times
- [ ] Verify background tasks running
- [ ] Check disk space

### Weekly

- [ ] Review performance metrics
- [ ] Check for failed jobs
- [ ] Review user feedback
- [ ] Update documentation if needed

### Monthly

- [ ] Test backup restore
- [ ] Review security logs
- [ ] Update dependencies (security patches)
- [ ] Optimize database
- [ ] Clean up old logs

### Quarterly

- [ ] Security audit
- [ ] Performance review
- [ ] Capacity planning
- [ ] Update documentation
- [ ] Review and update architecture

## Rollback Procedure

If issues occur during deployment:

1. **Database Rollback**:
   ```bash
   alembic downgrade -1
   ```

2. **Container Rollback**:
   ```bash
   docker-compose down
   git checkout <previous-commit>
   docker-compose up -d
   ```

3. **Verify Rollback**:
   - Check health endpoint
   - Test critical endpoints
   - Verify data integrity

## Emergency Contacts

- DevOps Lead: _______
- Database Admin: _______
- Security Team: _______
- On-Call Engineer: _______

## Quick Commands Reference

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Run migrations
docker-compose exec api alembic upgrade head

# Access database
docker-compose exec postgres psql -U medical_user adaptive_medical_learning

# Restart service
docker-compose restart api

# Scale workers
docker-compose up -d --scale celery_worker=3

# Check health
curl http://localhost:8000/health
```

## Troubleshooting

### API Not Starting
1. Check logs: `docker-compose logs api`
2. Verify DATABASE_URL is correct
3. Check if port 8000 is available
4. Verify all environment variables set

### Database Connection Failed
1. Check PostgreSQL is running
2. Verify credentials in .env
3. Check network connectivity
4. Verify pgvector extension installed

### Redis Connection Failed
1. Check Redis is running: `redis-cli ping`
2. Verify REDIS_URL in .env
3. Check firewall rules

### PDF Upload Failing
1. Check uploads directory exists and is writable
2. Verify file size limits
3. Check OpenAI API key is valid
4. Review celery worker logs

### Slow Performance
1. Check database indexes
2. Review slow query logs
3. Monitor memory usage
4. Check connection pool settings
5. Consider adding caching

---

**Remember**: Always test in staging environment before deploying to production!
