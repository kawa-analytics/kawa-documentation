# Security & Trust

At KAWA, protecting customer data and systems is a core part of how we build and operate our platform. Our security program is governed by documented policies, enforced through technical and organizational controls, and continuously monitored. This page summarizes the controls currently in place.

> KAWA uses Vanta for continuous security monitoring of its controls.

> This page describes how KAWA (the company) secures its operations and customer data. For in-product controls — roles, permissions, row-level security, and sharing — see [Data security & permissions](08_00_administration/08_02_security.md).

## 1. Encryption

* **In transit:** Confidential and sensitive data is encrypted when transmitted over public networks using secure transmission protocols. Remote access to production systems is permitted only over approved, encrypted connections.
* **At rest:** Datastores that hold sensitive customer data are encrypted at rest.
* **Key and media protection:** Privileged access to encryption keys is restricted to authorized users with a business need. Portable and removable media are encrypted when used.

## 2. Infrastructure security

Access to production infrastructure — databases, operating systems, applications, network, and firewalls — is restricted to authorized users with a documented business need. Authentication to production systems and the production network requires unique credentials (a unique username and password or authorized SSH keys), and privileged database authentication uses authorized secure mechanisms such as unique SSH keys.

The production environment is protected by:

* Firewalls, configured to prevent unauthorized access, with rulesets reviewed at least annually and required changes tracked to completion;
* Network segmentation to prevent unauthorized access to customer data;
* An intrusion detection system (IDS) for continuous monitoring and early detection of potential breaches;
* Log management and infrastructure performance monitoring, with alerts generated when predefined thresholds are met;
* Documented network and system hardening standards, based on industry best practices and reviewed at least annually;
* Routine patching of service infrastructure as part of maintenance and in response to identified vulnerabilities.

## 3. Access control

* Access to in-scope systems is based on job role and function, or requires a documented access request with manager approval before provisioning.
* The access control policy documents the requirements for adding new users, modifying users, and removing existing user access.
* Access reviews are conducted at least quarterly, and required changes are tracked to completion.
* Remote access to production systems requires a valid multi-factor authentication (MFA) method.
* Passwords for in-scope system components are configured according to the company password policy.

## 4. Secure development practices

* A formal Software Development Life Cycle (SDLC) methodology governs development, acquisition, implementation, changes (including emergency changes), and maintenance of information systems.
* Changes to software and infrastructure components are authorized, formally documented, tested, reviewed, and approved before being implemented in production. Access to migrate changes to production is restricted to authorized personnel.
* A configuration management procedure ensures system configurations are deployed consistently across the environment.
* Penetration testing is performed at least annually, with a remediation plan developed and changes implemented in accordance with SLAs.
* Host-based vulnerability scans are performed at least quarterly on external-facing systems; critical and high vulnerabilities are tracked to remediation.

## 5. Incident response and resilience

* Documented security and privacy incident response policies are communicated to authorized users, and the incident response plan is tested at least annually.
* Incidents are logged, tracked, resolved, and communicated to affected or relevant parties in accordance with the incident response policy and procedures.
* Business Continuity and Disaster Recovery (BC/DR) plans are established and tested at least annually.
* Backup and recovery requirements for customer data are documented in the data backup policy.
* The company maintains cybersecurity insurance to mitigate the financial impact of business disruptions.

## 6. Organizational and personnel security

* Background checks are performed on new employees.
* Employees complete security awareness training within thirty days of hire and at least annually thereafter.
* Employees and contractors acknowledge a Code of Conduct and sign confidentiality agreements.
* Company devices are centrally managed through a Mobile Device Management (MDM) system. Anti-malware technology is deployed to susceptible environments and is updated routinely, logged, and installed on relevant systems.
* A formal inventory of production assets is maintained. Electronic media containing confidential information is purged or destroyed in accordance with best practices, with certificates of destruction issued for each device destroyed.
* Physical access to data centers and secure areas is governed by documented processes, visitor sign-in and escort procedures, and is reviewed at least annually.

## 7. Data and privacy

* Formal retention and disposal procedures guide the secure retention and disposal of company and customer data.
* A data classification policy helps ensure confidential data is properly secured and restricted to authorized personnel.
* When a customer leaves the service, customer data containing confidential information is purged or removed from the application environment in accordance with best practices.

## 8. Risk and vendor management

* A documented risk management program provides guidance on identifying potential threats, rating the significance of associated risks, and defining mitigation strategies. Risk assessments are performed at least annually and include consideration of the potential for fraud.
* A vendor management program maintains a critical third-party vendor inventory, defines vendor security and privacy requirements, and reviews critical vendors at least annually.
* Written agreements with vendors and third parties include confidentiality and privacy commitments.

## 9. Governance

* Roles and responsibilities for the design, development, implementation, operation, maintenance, and monitoring of security controls are formally assigned.
* Information security policies and procedures are documented and reviewed at least annually.
* The board of directors maintains a documented charter and is briefed by senior management at least annually on the state of the company's cybersecurity and privacy risk.
* A formalized whistleblower policy and an anonymous reporting channel are in place.

## 10. Compliance and certifications

KAWA uses Vanta to continuously monitor its security controls.
