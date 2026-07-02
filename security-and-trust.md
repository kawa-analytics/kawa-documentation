# Security & Trust

KAWA is committed to protecting our customers' data and systems. Our security program is governed by documented policies and enforced through technical and organizational controls that are continuously monitored. This page lists the controls currently in place across our infrastructure, organization, product, internal procedures, and data handling, so customers, prospects, and auditors can see exactly how we protect information.

> KAWA uses Vanta for continuous security monitoring of its controls.

> This page describes how KAWA (the company) secures its operations and customer data. For in-product controls — roles, permissions, row-level security, and sharing — see Data security & permissions.

## 1. Infrastructure security

* **Unique production database authentication enforced.** Authentication to production datastores uses authorized secure authentication mechanisms, such as a unique SSH key.
* **Encryption key access restricted.** Privileged access to encryption keys is restricted to authorized users with a business need.
* **Unique account authentication enforced.** Authentication to systems and applications uses a unique username and password or authorized Secure Socket Shell (SSH) keys.
* **Production application access restricted.** System access is restricted to authorized access only.
* **Access control procedures established.** The access control policy documents the requirements for adding new users, modifying users, and removing an existing user's access.
* **Production database access restricted.** Privileged access to databases is restricted to authorized users with a business need.
* **Firewall access restricted.** Privileged access to the firewall is restricted to authorized users with a business need.
* **Production OS access restricted.** Privileged access to the operating system is restricted to authorized users with a business need.
* **Production network access restricted.** Privileged access to the production network is restricted to authorized users with a business need.
* **Unique network system authentication enforced.** Authentication to the production network uses unique usernames and passwords or authorized SSH keys.
* **Remote access MFA enforced.** Production systems can only be remotely accessed by authorized employees using a valid multi-factor authentication (MFA) method.
* **Remote access encrypted enforced.** Production systems can only be remotely accessed by authorized employees via an approved encrypted connection.
* **Intrusion detection system utilized.** An intrusion detection system provides continuous monitoring of the network and early detection of potential security breaches.
* **Log management utilized.** A log management tool is used to identify events that may have a potential impact on the company's ability to achieve its security objectives.
* **Infrastructure performance monitored.** An infrastructure monitoring tool monitors systems, infrastructure, and performance, and generates alerts when predefined thresholds are met.
* **Network segmentation implemented.** The network is segmented to prevent unauthorized access to customer data.
* **Network firewalls reviewed.** Firewall rulesets are reviewed at least annually, and required changes are tracked to completion.
* **Network firewalls utilized.** Firewalls are used and configured to prevent unauthorized access.
* **Network and system hardening standards maintained.** Network and system hardening standards are documented, based on industry best practices, and reviewed at least annually.
* **Service infrastructure maintained.** Infrastructure supporting the service is patched as part of routine maintenance and as a result of identified vulnerabilities, helping ensure servers are hardened against security threats.

## 2. Organizational security

* **Asset disposal procedures utilized.** Electronic media containing confidential information is purged or destroyed in accordance with best practices, and certificates of destruction are issued for each device destroyed.
* **Production inventory maintained.** A formal inventory of production system assets is maintained.
* **Portable media encrypted.** Portable and removable media devices are encrypted when used.
* **Anti-malware technology utilized.** Anti-malware technology is deployed to environments commonly susceptible to malicious attacks and is configured to be updated routinely, logged, and installed on all relevant systems.
* **Employee background checks performed.** Background checks are performed on new employees.
* **Code of Conduct acknowledged by contractors.** Contractor agreements include a code of conduct or a reference to the company code of conduct.
* **Code of Conduct acknowledged by employees and enforced.** Employees acknowledge a code of conduct at the time of hire. Employees who violate the code of conduct are subject to disciplinary action in accordance with a disciplinary policy.
* **Confidentiality Agreement acknowledged by contractors.** Contractors sign a confidentiality agreement at the time of engagement.
* **Confidentiality Agreement acknowledged by employees.** Employees sign a confidentiality agreement during onboarding.
* **Password policy enforced.** Passwords for in-scope system components are configured according to the company's policy.
* **MDM system utilized.** A mobile device management (MDM) system is in place to centrally manage mobile devices supporting the service.
* **Visitor procedures enforced.** Visitors are required to sign in, wear a visitor badge, and be escorted by an authorized employee when accessing the data center or secure areas.
* **Security awareness training implemented.** Employees complete security awareness training within thirty days of hire and at least annually thereafter.

## 3. Product security

* **Data encryption utilized.** Datastores housing sensitive customer data are encrypted at rest.
* **Company uses Vanta for continuous security monitoring.** The company uses Vanta for continuous security monitoring.
* **Penetration testing performed.** Penetration testing is performed at least annually. A remediation plan is developed and changes are implemented to remediate vulnerabilities in accordance with SLAs.
* **Data transmission encrypted.** Secure data transmission protocols are used to encrypt confidential and sensitive data when transmitted over public networks.
* **Vulnerability and system monitoring procedures established.** Formal policies outline the requirements for vulnerability management and system monitoring functions related to IT / Engineering.

## 4. Internal security procedures

* **Continuity and Disaster Recovery plans established.** Business Continuity and Disaster Recovery plans are in place that outline communication plans to maintain information security continuity in the event of the unavailability of key personnel.
* **Continuity and Disaster Recovery plans tested.** A documented Business Continuity/Disaster Recovery (BC/DR) plan is maintained and tested at least annually.
* **Cybersecurity insurance maintained.** Cybersecurity insurance is maintained to mitigate the financial impact of business disruptions.
* **Configuration management system established.** A configuration management procedure is in place to ensure that system configurations are deployed consistently throughout the environment.
* **Change management procedures enforced.** Changes to software and infrastructure components of the service are authorized, formally documented, tested, reviewed, and approved prior to being implemented in the production environment.
* **Production deployment access restricted.** Access to migrate changes to production is restricted to authorized personnel.
* **Development lifecycle established.** A formal systems development life cycle (SDLC) methodology governs the development, acquisition, implementation, changes (including emergency changes), and maintenance of information systems and related technology requirements.
* **SOC 2 – System Description.** A system description is maintained for Section III of the SOC 2 audit report.
* **Whistleblower policy established.** A formalized whistleblower policy is established, and an anonymous communication channel is in place for users to report potential issues or fraud concerns.
* **Board oversight briefings conducted.** The board of directors or a relevant subcommittee is briefed by senior management at least annually on the state of the company's cybersecurity and privacy risk, and provides feedback and direction to management as needed.
* **Board charter documented.** The board of directors has a documented charter that outlines its oversight responsibilities for internal control.
* **Board expertise developed.** Board members have sufficient expertise to oversee management's ability to design, implement, and operate information security controls. The board engages third-party information security experts and consultants as needed.
* **Board meetings conducted.** The board of directors meets at least annually and maintains formal meeting minutes. The board includes directors that are independent of the company.
* **Backup processes established.** The data backup policy documents requirements for backup and recovery of customer data.
* **System changes externally communicated.** Customers are notified of critical system changes that may affect their processing.
* **Management roles and responsibilities defined.** Management has established defined roles and responsibilities to oversee the design and implementation of information security controls.
* **Organization structure documented.** An organizational chart is maintained that describes the organizational structure and reporting lines.
* **Roles and responsibilities specified.** Roles and responsibilities for the design, development, implementation, operation, maintenance, and monitoring of information security controls are formally assigned in job descriptions and/or the Roles and Responsibilities policy.
* **Security policies established and reviewed.** Information security policies and procedures are documented and reviewed at least annually.
* **Support system available.** An external-facing support system is in place that allows users to report system information on failures, incidents, concerns, and other complaints to appropriate personnel.
* **System changes communicated.** System changes are communicated to authorized internal users.
* **Access reviews conducted.** Access reviews are conducted at least quarterly for in-scope system components to help ensure that access is restricted appropriately. Required changes are tracked to completion.
* **Access requests required.** User access to in-scope system components is based on job role and function, or requires a documented access request form and manager approval prior to access being provisioned.
* **Incident response plan tested.** The incident response plan is tested at least annually.
* **Incident response policies established.** Security and privacy incident response policies and procedures are documented and communicated to authorized users.
* **Incident management procedures followed.** Security and privacy incidents are logged, tracked, resolved, and communicated to affected or relevant parties by management according to the company's security incident response policy and procedures.
* **Physical access processes established.** Processes are in place for granting, changing, and terminating physical access to company data centers based on an authorization from control owners.
* **Data center access reviewed.** Access to the data centers is reviewed at least annually.
* **External support resources available.** Guidelines and technical support resources relating to system operations are provided to customers.
* **Service description communicated.** A description of the company's products and services is provided to internal and external users.
* **Risk assessment objectives specified.** The company specifies its objectives to enable the identification and assessment of risk related to those objectives.
* **Risks assessments performed.** Risk assessments are performed at least annually. As part of this process, threats and changes (environmental, regulatory, and technological) to service commitments are identified and the risks are formally assessed. The risk assessment includes a consideration of the potential for fraud and how fraud may impact the achievement of objectives.
* **Risk management program established.** A documented risk management program is in place that includes guidance on the identification of potential threats, rating the significance of the risks associated with the identified threats, and mitigation strategies for those risks.
* **Third-party agreements established.** Written agreements are in place with vendors and related third parties. These agreements include confidentiality and privacy commitments applicable to that entity.
* **Vendor management program established.** A vendor management program is in place, including a critical third-party vendor inventory, vendor security and privacy requirements, and a review of critical third-party vendors at least annually.
* **Vulnerabilities scanned and remediated.** Host-based vulnerability scans are performed at least quarterly on all external-facing systems. Critical and high vulnerabilities are tracked to remediation.

## 5. Data and privacy

* **Data retention procedures established.** Formal retention and disposal procedures are in place to guide the secure retention and disposal of company and customer data.
* **Customer data deleted upon leaving.** Customer data containing confidential information is purged or removed from the application environment, in accordance with best practices, when customers leave the service.
* **Data classification policy established.** A data classification policy is in place to help ensure that confidential data is properly secured and restricted to authorized personnel.
