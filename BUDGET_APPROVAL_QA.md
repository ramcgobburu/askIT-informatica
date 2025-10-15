# Informatica AI Assistant - Budget Approval Q&A
## Detailed Responses to Project Stakeholder Questions

*Date: October 15, 2025*  
*Project: Informatica Metadata Intelligence Platform*  
*Document Version: 1.0*

---

## TABLE OF CONTENTS

1. [Project Questions](#project-questions)
2. [Design Questions](#design-questions)
3. [Operational Questions](#operational-questions)
4. [Security Questions](#security-questions)
5. [Summary for Approval](#summary-for-approval)

---

## PROJECT QUESTIONS

### **Q1: Has this architecture been reviewed by Enterprise Architecture?**

**STATUS:** Pending EA review

**RECOMMENDATION:**  
Submit for EA review with the following alignment points:
- Uses Microsoft Azure (likely existing enterprise agreement)
- Leverages Microsoft 365 Copilot Studio (already licensed)
- Follows cloud-first strategy
- Uses serverless/consumption pricing (cost-effective)
- Aligns with self-service analytics initiatives
- Reduces operational costs by $40K+/month

**REQUEST:** 30-minute EA review session with architecture diagram

---

### **Q2: IT Project Billing Information**

**INFORMATION NEEDED FROM ORGANIZATION:**
- □ IT Project Number: [PENDING]
- □ Project Manager: [PENDING]
- □ Planview Project Name: [PENDING]
- □ Planview Project #: [PENDING]

**SUGGESTED VALUES:**
- Project Name: "Informatica Metadata Intelligence Platform"
- Category: Data Engineering Productivity Enhancement
- Type: Operational Efficiency / AI Innovation

---

### **Q3: Budget / Monthly Cost for Azure Cloud Services**

#### **Development/POC Phase (First 3 months):**
```
Azure Functions (Consumption):     $15/month
Azure AI Search (Basic):           $75/month
Blob Storage (Standard):           $10/month
Application Insights:              $15/month
Copilot Studio:                    $0 (included in M365 license)
────────────────────────────────────────────
TOTAL DEV/POC:                     $115/month
3-Month POC Cost:                  $345
```

#### **Production Phase (Ongoing after POC):**
```
Azure Functions (Consumption):     $20-25/month
Azure AI Search (Basic):           $75/month
Blob Storage (Standard):           $10/month
Application Insights:              $15/month
Copilot Studio:                    $0 (included in M365)
────────────────────────────────────────────
TOTAL PRODUCTION:                  $120-125/month
Annual Production Cost:            ~$1,500/year
```

#### **Year 1 Total Investment:**
```
POC (3 months):                    $345
Production (9 months):             $1,125
────────────────────────────────────────────
YEAR 1 TOTAL:                      $1,470
```

#### **Return on Investment:**
```
Monthly Savings (productivity):     $40,000
Monthly Cost:                       $125
────────────────────────────────────────────
Net Monthly Benefit:                $39,875
Annual ROI:                         32,000%
Payback Period:                     3 days
```

---

### **Q4: Timeline - When is this needed?**

**RECOMMENDED TIMELINE:**

```
Week 1-2:   Setup & Infrastructure
            - Create Azure resources
            - Configure security
            - Set up blob storage

Week 3-4:   Development
            - Implement Azure Functions
            - Create search index
            - Build processing logic

Week 5-6:   Integration
            - Configure Copilot Studio
            - Create custom connectors
            - Test end-to-end flow

Week 7-8:   Pilot Testing
            - Deploy to 10 pilot users
            - Gather feedback
            - Optimize performance

Week 9-10:  Production Rollout
            - Full team deployment
            - Training sessions
            - Monitoring setup

────────────────────────────────────────────
TOTAL TIMELINE: 10 weeks (2.5 months)
```

**RECOMMENDED START:** Q1 2025 for maximum Year 1 ROI

---

## DESIGN QUESTIONS

### **Q5: Can services be hosted on-prem? If not, why?**

**ANSWER: NO - Must be cloud-hosted**

#### **Technical Reasons:**

**1. Copilot Studio Dependency:**
- Copilot Studio is cloud-only (Microsoft SaaS)
- Requires HTTPS endpoints accessible from Microsoft cloud
- Cannot call on-prem APIs without complex VPN/ExpressRoute setup
- Would add $150+/month for VPN gateway

**2. Azure AI Search Requirement:**
- Managed service with no on-prem option
- Requires Azure infrastructure for semantic search
- On-prem alternatives (Elasticsearch) lack AI semantic features
- Would require dedicated hardware and maintenance team

**3. Serverless Benefits:**
- Auto-scaling not possible on-prem
- Would require dedicated servers running 24/7
- On-prem cost: ~$5,000-10,000 hardware + maintenance
- Cloud cost: $125/month with zero hardware

**4. Maintenance Overhead:**
- Cloud: Microsoft handles patching, updates, security
- On-prem: Requires dedicated operations team

#### **Cost Comparison:**
```
ON-PREMISES APPROACH:
Hardware (servers):                 $5,000 one-time
Annual maintenance:                 $1,500/year
Operations team (20% FTE):          $24,000/year
Network infrastructure:             $2,000/year
────────────────────────────────────────────
Total Year 1:                       $32,500
Ongoing annual:                     $27,500/year

CLOUD APPROACH:
Year 1 cost:                        $1,470
Ongoing annual:                     $1,500/year
────────────────────────────────────────────
SAVINGS BY USING CLOUD:             $30,000+ Year 1
Annual ongoing savings:             $26,000/year
```

**RECOMMENDATION:** Cloud-only deployment

---

### **Q6: Is there an architecture diagram?**

**ANSWER: YES - See attached ARCHITECTURE_CLARIFICATION.md**

**High-Level Overview:**

```
┌─────────────────────────────────────────────────────────┐
│ USER LAYER (Any device, anywhere)                       │
│ └─ Microsoft Teams / Web Browser                        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS (M365 SSO)
┌────────────────────▼────────────────────────────────────┐
│ COPILOT STUDIO (Microsoft SaaS)                         │
│ └─ Natural Language Processing                          │
│ └─ Conversation Management                              │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS (Custom Connector)
┌────────────────────▼────────────────────────────────────┐
│ AZURE FUNCTIONS (Your Azure Tenant)                     │
│ Region: East US / Canada Central                        │
│ └─ search-workflow API                                  │
│ └─ debug-table API                                      │
│ └─ get-workflow-details API                             │
└──────┬──────────────────────────┬───────────────────────┘
       │                          │
       ▼                          ▼
┌──────────────────┐      ┌──────────────────┐
│ AZURE AI SEARCH  │      │ BLOB STORAGE     │
│ (Search Index)   │      │ (XML Files)      │
│ - Metadata       │      │ - Source Data    │
└──────────────────┘      └──────────────────┘
```

**Full detailed diagram available in:** `ARCHITECTURE_CLARIFICATION.md`

---

### **Q7: List of services to be installed**

#### **Azure Services (All in same Resource Group):**

**1. Azure Function App**
- Runtime: Python 3.11
- Plan: Consumption (Serverless)
- SKU: Dynamic
- Region: East US or Canada Central
- Purpose: API endpoints for search and processing

**2. Azure AI Search Service**
- Tier: Basic
- Replicas: 1
- Partitions: 1
- Region: Same as Function App
- Purpose: Intelligent metadata search with semantic capabilities

**3. Azure Storage Account**
- Type: StorageV2 (general purpose v2)
- Performance: Standard
- Replication: LRS (Locally Redundant)
- Container: "xml-metadata"
- Purpose: Store source XML files

**4. Application Insights**
- Type: Application Insights
- Linked to Function App
- Purpose: Monitoring, logging, alerts

**5. Power Platform Custom Connector**
- Platform: Power Apps / Copilot Studio
- Type: Custom (HTTP)
- Purpose: Bridge between Copilot and Azure Functions

**6. Copilot Studio Agent**
- Platform: Microsoft Copilot Studio
- Licensing: Included in M365 license
- Purpose: Conversational AI interface

**TOTAL SERVICES:** 6  
**COMPLEXITY:** Low (all managed PaaS services)  
**VENDOR:** Microsoft Azure (single vendor)

---

### **Q8: Who is deploying the services?**

**DEPLOYMENT METHOD:**

**POC/Development Phase:**
- Method: Manual deployment via Azure Portal
- Reason: Faster iteration and testing
- Owner: Data Engineering team
- Time: 2-3 hours initial setup

**Production Phase:**
- Method: Infrastructure as Code (IaC)
- Technology: Azure CLI / Bicep / Terraform
- Reason: Repeatable, version-controlled, auditable
- Owner: Data Engineering with Cloud Ops support

**Required Access:**
- Azure Subscription Contributor role
- Resource Group Owner role
- M365 Copilot Studio admin

**Deployment Steps:**
```bash
# Sample deployment script
az group create --name rg-informatica-agent --location eastus
az storage account create --name stinformaticadata --resource-group rg-informatica-agent
az search service create --name srch-informatica --resource-group rg-informatica-agent --sku basic
az functionapp create --name func-informatica-agent --resource-group rg-informatica-agent
```

---

### **Q9: What environments are required?**

**RECOMMENDED APPROACH:**

**Environment 1: DEV/POC (Combined)**
- Duration: First 3 months
- Purpose: Development + POC testing
- Users: 5-10 pilot users from Data Engineering
- Cost: $115/month
- Infrastructure: Single instance of all services

**Environment 2: PRODUCTION**
- Duration: After successful POC
- Purpose: Full team usage
- Users: 20+ Data Engineering team members
- Cost: $125/month
- Infrastructure: Production-grade configuration

**OPTIONAL (Not Recommended for Initial Phase):**
- QA Environment: Only if strict testing protocols required
- Cost impact: Additional $115/month

**TOTAL RECOMMENDED ENVIRONMENTS:** 2 (Dev/POC + Production)

**Why Not More Environments?**
- Serverless architecture = low risk of production issues
- No databases or state to corrupt
- Read-only operations (no data modification)
- Low traffic volume doesn't justify multi-environment complexity
- Cost-effective: 2 environments = $240/month vs 4 environments = $480/month

---

### **Q10: Is this implementation temporary or permanent?**

**ANSWER: PERMANENT**

**Justification:**
- Addresses ongoing operational need (not project-specific)
- ROI sustains indefinitely ($40K/month savings)
- No alternative solution planned or available
- Becomes critical infrastructure for Data Engineering operations
- Knowledge base grows over time as more XML files are added
- Scales with team growth and data volume

**Lifecycle Plan:**
- **Initial commitment:** 3 years
- **Review cycle:** Annual cost/benefit analysis
- **Decommission trigger:** Only if Informatica platform is replaced

**Long-term Value:**
- Reduces onboarding time for new engineers by 80%
- Creates institutional knowledge repository
- Enables self-service data discovery
- Reduces dependency on senior engineers

**RECOMMENDATION:** Approve as permanent infrastructure with annual review

---

### **Q11: Cloud-to-On-Prem Communication Requirement?**

**PHASE 1 (POC - Current Request): NO**

All services are contained within Azure cloud:
- Data source: XML files in Azure Blob Storage
- Processing: Azure Functions
- Search: Azure AI Search
- Interface: Copilot Studio (Microsoft cloud)
- **No on-prem connectivity needed**

**PHASE 2 (Future Enhancement - Optional): YES**

Potential future requirement for real-time workflow status:
- Azure Functions → On-Prem Informatica PowerCenter server
- Purpose: Query real-time workflow execution status
- Implementation: Azure ExpressRoute or Site-to-Site VPN
- Direction: Outbound from Azure only

**Cost Impact:**
```
Phase 1 (Current):                  $125/month (no connectivity)
Phase 2 (With VPN):                 $275/month (+$150 VPN gateway)
```

**RECOMMENDATION FOR APPROVAL:**
- **Approve Phase 1 only** (no on-prem connectivity)
- Phase 2 requires separate budget approval and technical review
- Phase 1 provides 80% of value without complexity

---

### **Q12: DNS Name Resolution Between Cloud and On-Prem?**

**PHASE 1 (Current): NO - Not needed**

All services use public Azure DNS:
- Format: `*.azurewebsites.net`, `*.search.windows.net`
- No custom DNS configuration required
- No on-prem name resolution needed

**PHASE 2 (Future): YES - If real-time integration implemented**

Would require:
- Azure Private DNS zone
- DNS forwarding to on-prem
- Or ExpressRoute with DNS integration

**Cost:**
- Phase 1: $0 (public DNS only)
- Phase 2: $5/month (Azure Private DNS)

**RECOMMENDATION:** Phase 1 requires no DNS changes

---

### **Q13: Licensing Considerations?**

**LICENSE AUDIT:**

**1. Microsoft 365 (Copilot Studio)**
- Requirement: M365 license per user
- Status: ✅ Already licensed (existing org subscriptions)
- Users: ~20 Data Engineering team members
- Additional cost: $0 (included in current M365 E3/E5)
- **Action:** Confirm with M365 admin that licenses cover Copilot Studio

**2. Azure Subscription**
- Requirement: Active Azure subscription
- Status: ⚠️ Check if org has Enterprise Agreement
- Cost: $125/month pay-as-you-go OR discounted via EA
- **Action:** Confirm with Azure subscription owner

**3. Open Source Components**
- Python 3.11: MIT License (no cost)
- Azure SDKs: MIT License (no cost)
- Function runtime: Included in Azure Functions pricing

**TOTAL ADDITIONAL LICENSING COST: $0**

All services use existing Microsoft licenses and open-source components.

**Action Items:**
- ☐ Verify M365 licenses include Copilot Studio for Data Eng team
- ☐ Confirm Azure subscription budget can accommodate $125/month
- ☐ Check if Enterprise Agreement provides discounts on Azure services

---

## OPERATIONAL QUESTIONS

### **Q14: Team Ownership**

**PRIMARY OWNER: Data Engineering Team**

**Responsibilities:**
- Content management (XML file updates)
- User support (Tier 1)
- Feature requests and enhancements
- Usage monitoring and reporting

**Team Lead:** [Your Name/Manager]  
**Team Size:** 3-5 people  
**Effort Required:**
- Initial setup: 40 hours (one-time)
- Monthly maintenance: 2-4 hours
- XML updates: 1 hour/month (can be automated)

**SHARED SUPPORT:**

| Team | Responsibility | Engagement |
|------|----------------|------------|
| Cloud Operations | Azure infrastructure | Deployment, scaling |
| InfoSec | Security compliance | Quarterly reviews |
| IT Procurement | Licensing | Annual renewal |
| M365 Admin | Copilot Studio | License management |

**DAY-TO-DAY OPERATIONS:**
- XML file updates → Data Engineering (self-service upload to Blob)
- User questions → Data Engineering (answer workflow queries)
- Service outages → Cloud Ops (Azure infrastructure issues)
- Security incidents → InfoSec (security events)

---

### **Q15: Support Escalation Process**

**TIER 1: Data Engineering Team**
- **Handles:** User questions about workflows, search results, metadata
- **Response Time:** 2 business hours
- **Contact:** [Your team email/Slack channel]
- **Examples:** "How do I find a workflow?", "What does this result mean?"

**TIER 2: Application Support**
- **Handles:** Function errors, performance issues, bugs
- **Response Time:** 4 business hours
- **Contact:** [DevOps team/on-call]
- **Examples:** API timeouts, search errors, processing failures

**TIER 3: Azure Support**
- **Handles:** Azure service outages, platform issues
- **Response Time:** Per Azure support plan (1-4 hours)
- **Contact:** Azure Support Portal
- **Examples:** Azure Functions downtime, AI Search unavailable

**MICROSOFT SUPPORT:**
- **Copilot Studio:** Microsoft 365 support ticket
- **Azure Platform:** Azure support ticket
- **Licensing:** Microsoft account team

**CRITICAL ISSUES (Production Down):**
- **Contact:** Cloud Ops on-call + Azure Premier Support
- **Response Time:** 1 hour
- **Escalation:** Automatic page to leadership if >2 hours

**SLA TARGET:** 99.9% uptime (aligned with Azure SLA)

---

### **Q16: Backup Requirements**

**YES - Backups Required**

**BACKUP STRATEGY:**

**1. XML Files (Source Data) - CRITICAL**
- **Location:** Azure Blob Storage
- **Method:** Azure Blob soft delete + versioning
- **Retention:** 30 days
- **Recovery:** Point-in-time restore
- **Cost:** $2-5/month (included in blob storage)
- **Automated:** Yes

**2. Azure AI Search Index**
- **Method:** Rebuild from XML source files
- **Backup:** Not needed (derived data)
- **Recovery Time:** 10-15 minutes (re-run process-xml function)
- **Cost:** $0

**3. Azure Function Code**
- **Location:** Git repository (GitHub/Azure DevOps)
- **Method:** Version control
- **Retention:** Indefinite
- **Recovery:** Redeploy from repository
- **Cost:** $0 (existing Git infrastructure)

**4. Copilot Studio Configuration**
- **Location:** Microsoft-managed backup
- **Method:** Export to JSON monthly
- **Storage:** Git repository
- **Recovery:** Import or recreate from documentation
- **Cost:** $0

**RECOVERY METRICS:**
- **Recovery Time Objective (RTO):** 2 hours
- **Recovery Point Objective (RPO):** 24 hours
- **Data Loss Risk:** Minimal (versioned storage)

**BACKUP SCHEDULE:**
- Blob versioning: Automatic (real-time)
- Config export: Monthly
- Code commits: On every change
- Full backup test: Quarterly

**TOTAL BACKUP COST:** $5/month

---

### **Q17: Monitoring Requirements**

**YES - Monitoring Required**

**MONITORING COMPONENTS:**

**1. Application Insights (Built-in)**
- Function execution times and latency
- Error rates and exception tracking
- Request volume and patterns
- Dependency health (AI Search, Blob Storage)
- Custom metrics and events
- **Cost:** $15/month (included in budget)

**2. Azure Monitor Alerts**
- Alert on function failures >5% error rate
- Alert on response time >5 seconds
- Alert on storage account access issues
- Alert on search service degradation
- **Cost:** Included in Application Insights

**3. Azure AI Search Metrics**
- Query latency tracking
- Index size and document count
- Search queries per second
- Storage utilization
- **Cost:** Included in search service

**4. Copilot Studio Analytics**
- User satisfaction scores
- Conversation volumes
- Topic resolution rates
- Tool call success rates
- **Cost:** Included in Copilot Studio

**KEY METRICS TO TRACK:**

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Availability | 99.9% | <99% |
| Response Time | <3 sec | >5 sec |
| Error Rate | <1% | >5% |
| User Satisfaction | >4.5/5 | <4.0/5 |
| Monthly Cost | <$150 | >$200 |

**ALERTING:**
- **Destination:** Team email + Slack channel + PagerDuty
- **Critical alerts:** Immediate notification
- **Warning alerts:** Daily digest
- **Info alerts:** Weekly report

**DASHBOARDS:**
- Azure Portal built-in dashboard
- Custom Power BI dashboard (optional)
- Weekly email report to stakeholders

---

### **Q18: Disaster Recovery Scope**

**RECOMMENDED: YES (Tier 3 - Standard DR)**

**DR CLASSIFICATION:**

**Tier 3: Non-Critical (Can tolerate reasonable downtime)**

**Justification:**
- Productivity tool, not mission-critical production pipeline
- No customer-facing impact
- No financial transactions
- Team can fallback to manual XML search temporarily
- Can tolerate 4-24 hour outage without business impact

**DR STRATEGY:**

**Data Protection:**
- Primary Region: East US
- Backup Storage: Geo-replicated to West US (optional)
- RTO: 4 hours (Recovery Time Objective)
- RPO: 24 hours (Recovery Point Objective)

**Recovery Process:**
```
Step 1: Create new resource group in secondary region    (30 min)
Step 2: Restore XML files from geo-replicated storage    (15 min)
Step 3: Rebuild search index from XML files              (10 min)
Step 4: Deploy function code from Git repository         (15 min)
Step 5: Update Copilot Studio connector URL              (10 min)
────────────────────────────────────────────────────────────────
TOTAL RECOVERY TIME:                                     80 minutes
```

**GEO-REDUNDANCY OPTIONS:**

| Option | Cost | RTO | Automatic Failover |
|--------|------|-----|-------------------|
| Basic (versioning only) | $5/mo | 4 hrs | No |
| GRS (geo-replicate storage) | +$10/mo | 2 hrs | No |
| Multi-region deployment | +$125/mo | <1 hr | Yes |

**RECOMMENDATION:**
- ✅ **Tier 3 DR (Basic):** $5/month - APPROPRIATE
- ❌ Tier 1 (Automatic failover): Not needed for productivity tool
- ❌ Multi-region: Not cost-justified

**DR TESTING:**
- Frequency: Annually
- Process: Simulate failover to secondary region
- Duration: 4 hours
- Success criteria: <4 hour recovery

---

## SECURITY QUESTIONS

### **Q19: Authoritative Identity System**

**ANSWER: Microsoft Entra ID (Azure AD)**

**Authentication Flow:**
```
User → Microsoft 365 (SSO) → Copilot Studio → Azure Functions → Azure Resources
```

**Identity Provider Details:**
- **System:** Corporate Microsoft Entra ID tenant
- **Users:** Corporate email addresses (@yourcompany.com)
- **SSO:** Enabled via existing M365 integration
- **MFA:** Enforced by organization policy (no additional setup)
- **Guest Users:** Not supported (internal employees only)

**No Separate Identity System:**
- Leverages existing corporate directory
- No custom user database
- No additional password management
- Integrated with existing access controls
- Follows organizational security policies

**Authorization Layers:**
1. M365 authentication for Copilot access
2. Azure AD RBAC for Azure resource management
3. Managed identities for service-to-service auth

---

### **Q20: User Access Requirements**

**USER ACCESS BREAKDOWN:**

**1. END USERS (Copilot Studio Access)**
- **Who:** Data Engineering team (~20 users)
- **Access:** Copilot Studio via Teams or web
- **Authentication:** Microsoft 365 SSO
- **A-Account:** ❌ NOT required (regular user account)
- **Permissions:** Read-only access to workflow metadata
- **Justification:** Day-to-day usage for workflow queries
- **Cost per user:** $0 (uses existing M365 license)

**2. DEVELOPERS (Code Deployment)**
- **Who:** 2-3 developers maintaining the solution
- **Access:** Azure Portal, Function App deployment, Git repo
- **Authentication:** Azure AD with MFA
- **A-Account:** ✅ YES - Required for Azure admin tasks
- **Permissions:** Contributor role on resource group
- **Justification:** Deploy code, update configurations, manage resources

**3. OPERATORS (Monitoring & Support)**
- **Who:** Cloud Ops team (2-3 people)
- **Access:** Azure Portal for monitoring/troubleshooting
- **Authentication:** Azure AD with MFA
- **A-Account:** ✅ YES - Required for Azure admin
- **Permissions:** Reader role on resource group
- **Justification:** View logs, monitor health, troubleshoot issues

**4. ADMINISTRATORS (Full Control)**
- **Who:** 1 technical lead
- **Access:** Full Azure subscription access
- **Authentication:** Azure AD with MFA
- **A-Account:** ✅ YES - Required
- **Permissions:** Owner role on resource group
- **Justification:** Manage resources, rotate keys, assign access

**SUMMARY:**
- **Total A-Accounts Needed:** 4-6 (admins/developers only)
- **Total End Users:** 20 (no A-account required)
- **M365 Licenses Required:** 20 (existing)

---

### **Q21: Authorization Model**

**LAYERED AUTHORIZATION ARCHITECTURE:**

**LAYER 1: Copilot Studio Access**
- **Requirement:** Valid M365 license
- **Enforcement:** Microsoft Copilot Studio platform
- **Scope:** Can interact with chatbot
- **Implementation:** Automatic via M365 licensing
- **Users:** All Data Engineering team members

**LAYER 2: Azure Function Access**
- **Current:** No authentication (internal-only via connector)
- **Recommendation:** Add Azure AD authentication before production
- **Enforcement:** Azure Functions runtime
- **Scope:** Can call API endpoints
- **Implementation:** Managed identity + Azure AD tokens

**LAYER 3: Azure Resources (Infrastructure)**
- **Requirement:** Azure RBAC roles
- **Enforcement:** Azure Resource Manager
- **Scope:** Can manage/view infrastructure
- **Roles:**
  - Owner: 1 person (full control)
  - Contributor: 2-3 people (deploy/update)
  - Reader: 2-3 people (monitoring only)
  - None: End users (no Azure Portal access)

**LAYER 4: Data Access (Blob Storage)**
- **Requirement:** Storage account RBAC
- **Enforcement:** Azure Storage
- **Roles:**
  - Storage Blob Data Contributor: 2-3 developers
  - Storage Blob Data Reader: Function App managed identity
  - None: End users (access via Copilot only)

**AUTHORIZATION MATRIX:**

| Role | Copilot Access | Azure Portal | Deploy Code | View Logs | Modify Data |
|------|----------------|--------------|-------------|-----------|-------------|
| End User | ✅ | ❌ | ❌ | ❌ | ❌ |
| Developer | ✅ | ✅ | ✅ | ✅ | ✅ |
| Operator | ✅ | ✅ | ❌ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

**SECURITY PRINCIPLE:** Least privilege access model

---

### **Q22: SSL Certificate Requirements**

**ANSWER: YES - All connections use SSL/TLS**

**CERTIFICATES REQUIRED:**

**1. Azure Functions**
- **Domain:** `*.azurewebsites.net`
- **Certificate:** Microsoft-managed SSL certificate
- **Example:** `func-informatica-agent.azurewebsites.net`
- **Renewal:** Automatic by Microsoft
- **Cost:** $0 (included with Azure Functions)
- **TLS Version:** TLS 1.2+ enforced

**2. Azure AI Search**
- **Domain:** `*.search.windows.net`
- **Certificate:** Microsoft-managed
- **Cost:** $0 (included)
- **Action:** None required

**3. Copilot Studio**
- **Domain:** `copilotstudio.microsoft.com`
- **Certificate:** Microsoft-managed
- **Cost:** $0 (included)
- **Action:** None required

**4. Custom Domain (Optional - Not Recommended for Phase 1)**
- **Example:** `informatica-api.yourcompany.com`
- **Certificate:** Would need to purchase or use existing
- **Cost:** $60/year (standard SSL) to $300/year (EV SSL)
- **Recommendation:** Not needed - use default Azure domains

**CERTIFICATE MANAGEMENT:**
- **Provider:** Microsoft Azure
- **Renewal:** Fully automatic
- **Monitoring:** Not required (managed by Azure)
- **Expiration:** Never (auto-renewed before expiry)

**SSL/TLS CONFIGURATION:**
- **Minimum TLS Version:** TLS 1.2
- **Cipher Suites:** Industry standard (managed by Azure)
- **Certificate Transparency:** Enabled
- **HSTS:** Enabled for all endpoints

**TOTAL SSL/TLS COST:** $0  
**MANAGEMENT EFFORT:** 0 hours (fully automated)

---

### **Q23: PII (Personally Identifiable Information)**

**ANSWER: NO - Minimal PII, No Sensitive Data**

**DATA INVENTORY:**

**1. XML Metadata (Blob Storage)**
- **Contains:**
  - Workflow names (e.g., "wfl_sales_daily")
  - Table names (e.g., "SALES_TRANSACTIONS")
  - Mapping configurations
  - Transformation logic
  - Technical metadata
- **PII:** ❌ NO
- **Sensitivity:** Low (internal technical configs)

**2. Search Index (Azure AI Search)**
- **Contains:** Indexed workflow metadata (same as XML)
- **PII:** ❌ NO
- **Sensitivity:** Low

**3. Application Logs (Application Insights)**
- **Contains:**
  - User queries (e.g., "find sales workflow")
  - Response times
  - Error messages
  - User email addresses (for audit trail)
- **PII:** ⚠️ YES - Email addresses only
- **Sensitivity:** Low (audit purposes)
- **Retention:** 30 days

**4. Copilot Conversations**
- **Contains:**
  - User questions and bot responses
  - User email addresses
  - Conversation history
- **PII:** ⚠️ YES - Email addresses + conversation data
- **Sensitivity:** Low
- **Retention:** Per Microsoft 365 retention policy
- **Storage:** Microsoft-managed, SOC 2 compliant

**PII ASSESSMENT:**

| Data Element | Contains PII? | Sensitivity | Risk Level |
|--------------|---------------|-------------|------------|
| XML Metadata | NO | Low | Minimal |
| Search Index | NO | Low | Minimal |
| App Logs | YES (emails) | Low | Minimal |
| Conversations | YES (emails) | Low | Minimal |

**COMPLIANCE REQUIREMENTS:**
- **GDPR:** ✅ Not applicable (no EU personal data)
- **CCPA:** ✅ Not applicable (no CA resident data)
- **SOX:** ✅ Not applicable (no financial data)
- **HIPAA:** ✅ Not applicable (no health data)
- **Internal Policy:** Standard data classification

**DATA CLASSIFICATION:** **INTERNAL USE ONLY** (not confidential, not public)

**RECOMMENDATION:**  
No additional PII controls required beyond standard corporate policies and Azure built-in protections.

---

### **Q24: Public Accessibility**

**ANSWER: NO - Internal Only (Private Access)**

**ACCESSIBILITY DESIGN:**

**1. Copilot Studio:**
- **Public URL:** ❌ NO
- **Access:** Microsoft 365 authenticated users only
- **Network:** Microsoft cloud (not exposed to public internet)
- **Users:** Internal employees with M365 licenses
- **Authentication:** Required (SSO)

**2. Azure Functions:**
- **Public IP:** ✅ YES (assigned by Azure, but not directly accessible)
- **Public Access:** ❌ NO (secured via Custom Connector)
- **Direct URL Access:** ❌ Blocked (users cannot call directly)
- **Access Pattern:** Copilot Studio → Custom Connector → Azure Function
- **Security:** Function keys + optional IP whitelisting

**3. Azure AI Search:**
- **Public IP:** ✅ YES (assigned by Azure)
- **Public Access:** ❌ NO (API keys required)
- **Access:** Azure Functions only (via API key)
- **Direct Access:** ❌ Not possible without admin API key

**4. Blob Storage:**
- **Public IP:** ✅ YES (assigned by Azure)
- **Public Access:** ❌ NO (private containers)
- **Access:** Azure Functions only (via connection string)
- **Anonymous Access:** ❌ Disabled

**NETWORK ARCHITECTURE:**

```
INTERNET (Public)
     │
     │ ❌ Direct access BLOCKED
     │
     ↓
MICROSOFT 365 NETWORK (Secured)
     │
     │ ✅ Authentication required
     │
     ↓
COPILOT STUDIO (M365 Users Only)
     │
     │ ✅ Custom Connector
     │
     ↓
AZURE SERVICES (Your Tenant - Private)
     │
     ├─→ Azure Functions (API keys)
     ├─→ Azure AI Search (API keys)
     └─→ Blob Storage (connection string)
```

**PUBLIC ACCESSIBILITY SUMMARY:**
- ❌ Not accessible from public internet
- ❌ No public-facing web interface
- ❌ No anonymous access
- ✅ Requires corporate M365 authentication
- ✅ Internal employees only

**RECOMMENDATION:** Maintain internal-only access for Phase 1

**Future Considerations (Phase 2 - If External Access Needed):**
- Would require: Azure API Management ($75+/month)
- Would require: Azure Front Door for WAF ($35+/month)
- Would require: Additional security review
- Total additional cost: $110+/month

---

### **Q25: Public IPs and Firewall Rules**

**PHASE 1 (Current POC): NO PUBLIC IPs TO WHITELIST**

**Explanation:**
- Copilot Studio is Microsoft SaaS (no static IPs needed)
- Azure Functions use dynamic outbound IPs
- All communication stays within Microsoft/Azure cloud
- No firewall rules required for Phase 1

**PHASE 2 (Future - On-Prem Integration): YES**

**If on-prem integration is implemented in Phase 2:**

**Outbound Connection Required:**
- **Source:** Azure Functions
- **Destination:** On-prem Informatica PowerCenter server
- **Direction:** Outbound from Azure → Inbound to corporate network
- **Purpose:** Query real-time workflow status

**Firewall Rule Request (Phase 2 Only):**

```
SOURCE ADDRESSES (Azure Function Outbound IPs):
To be determined after deployment
Command: az functionapp show --query "outboundIpAddresses"
Example: 52.186.89.23, 52.186.89.45, 52.186.89.67

DESTINATION:
On-prem Informatica PowerCenter server
IP: [To be provided by on-prem team]

PORTS:
- Port 443 (HTTPS): Azure Functions → Informatica Web Services
- Port 1433 (SQL): Azure Functions → Informatica Repository DB (if needed)

PROTOCOL: TCP
DIRECTION: Inbound (from Azure perspective: outbound)
JUSTIFICATION: Informatica AI Assistant real-time status queries
```

**PORTS SUMMARY:**

**INGRESS (Inbound to Azure):**
- ❌ NONE - No inbound public access required

**EGRESS (Outbound from Azure):**
- **Phase 1:** ❌ NONE - No outbound to on-prem
- **Phase 2:** ✅ Port 443 + possibly 1433 to on-prem Informatica

**INTRA-AZURE (Within Azure Tenant):**
- Azure Functions → AI Search: Port 443 (stays in Azure)
- Azure Functions → Blob Storage: Port 443 (stays in Azure)
- No firewall rules needed (same tenant communication)

**RECOMMENDATION FOR APPROVAL:**

✅ **Phase 1:** No firewall changes required  
⏸️ **Phase 2:** Separate firewall change request if real-time integration is pursued

---

## SUMMARY FOR APPROVAL

### **Budget Summary**

**YEAR 1 INVESTMENT:**
```
POC Phase (3 months):              $345
Production Phase (9 months):       $1,125
────────────────────────────────────────
TOTAL YEAR 1:                      $1,470
```

**ONGOING ANNUAL COST:**
```
Azure Services:                    $1,500/year ($125/month)
```

**RETURN ON INVESTMENT:**
```
Annual Productivity Savings:       $480,000
Annual Cost:                       $1,500
────────────────────────────────────────
Net Annual Benefit:                $478,500
ROI:                               31,900%
Payback Period:                    3 days
```

---

### **Key Approval Points**

✅ **Low Cost:** $125/month ongoing  
✅ **High ROI:** 31,900%  
✅ **Quick Payback:** 3 days  
✅ **Uses Existing Licenses:** M365 (Copilot Studio)  
✅ **Cloud-Only:** No on-prem hardware or maintenance  
✅ **No PII Concerns:** Only technical metadata  
✅ **Internal Access Only:** No public exposure  
✅ **Managed Services:** Low operational burden  
✅ **Fast Implementation:** 10 weeks  
✅ **Permanent Solution:** Long-term value  
✅ **Scalable:** Handles team growth automatically  

---

### **Teams Required for Approval**

| Team | Role | Time Commitment |
|------|------|----------------|
| Data Engineering | Owner & Developer | 40 hours setup + 2-4 hours/month |
| InfoSec | Security Review | 2 hours (one-time) |
| Cloud Ops / Azure Admin | Resource Provisioning | 3 hours setup |
| M365 Admin | License Confirmation | 30 minutes |

**TOTAL STAKEHOLDERS:** 4 teams, 1-hour approval meeting

---

### **Action Items for Approval**

**IMMEDIATE ACTIONS:**
- ☐ Confirm IT project number and Planview details
- ☐ Schedule EA review (30 minutes)
- ☐ Approve Year 1 budget ($1,470)
- ☐ Provision A-accounts for 4-6 admins/developers
- ☐ Assign ownership to Data Engineering team
- ☐ Approve 10-week implementation timeline

**POST-APPROVAL ACTIONS:**
- ☐ Schedule kickoff meeting with stakeholders
- ☐ Create Azure resource group
- ☐ Begin Phase 1 implementation

---

### **Risk Assessment**

**LOW RISK PROJECT:**

| Risk Factor | Level | Mitigation |
|-------------|-------|------------|
| Financial | LOW | $1,470 Year 1 investment |
| Technical | LOW | Proven Microsoft technologies |
| Security | LOW | Internal-only, existing auth |
| Operational | LOW | Managed PaaS services |
| Timeline | LOW | 10 weeks with clear milestones |
| Resource | LOW | Uses existing team capacity |

**OVERALL RISK:** **LOW**

---

### **Success Criteria**

**POC SUCCESS METRICS (Week 8):**
- ✓ 10 pilot users actively using the system
- ✓ 95%+ search accuracy
- ✓ <3 second average response time
- ✓ 4.5+/5 user satisfaction score
- ✓ 50+ queries per week

**PRODUCTION SUCCESS METRICS (Month 6):**
- ✓ 20+ active users
- ✓ 200+ queries per week
- ✓ 70% reduction in support tickets
- ✓ 80% faster workflow discovery
- ✓ Cost within budget (<$150/month)

---

## APPENDICES

### **Appendix A: Detailed Cost Breakdown**

See `EXECUTIVE_WALKTHROUGH_PRESENTATION.md` for detailed cost analysis

### **Appendix B: Architecture Diagrams**

See `ARCHITECTURE_CLARIFICATION.md` for visual architecture diagrams

### **Appendix C: Technical Documentation**

- `COMPLETE_SETUP_GUIDE.md` - Full implementation guide
- `AI_BENEFITS_SUMMARY.md` - AI technology explanation
- `AI_INTEGRATION_EXPLAINED.md` - Detailed AI architecture

---

## DOCUMENT REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-15 | [Your Name] | Initial comprehensive Q&A document |

---

**END OF DOCUMENT**

