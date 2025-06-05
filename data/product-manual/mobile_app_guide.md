# Mobile Banking App – Onboarding Guide

This guide helps new employees of **DigitalBank** understand the mobile app from a user-support perspective.

## 1. Installation
1. Download **DigitalBank** from the Apple App Store or Google Play.  
2. Verify the publisher: *DigitalBank S.A.*  
3. Enable automatic updates.

## 2. First Login
- Enter CPF and temporary PIN (sent via SMS).  
- Create a 6-digit app password.  
- Register Face ID or fingerprint (optional but recommended).

## 3. Account Dashboard
| Section     | Description                         |
|-------------|-------------------------------------|
| Balance     | Real-time account balance.          |
| Cards       | Virtual & physical card controls.   |
| Investments | Fixed income, CDBs, funds.          |
| Support     | 24 × 7 chat and FAQ.                |

## 4. Security Features
1. **Device Binding** – each device has a unique cryptographic key.  
2. **Transaction Signing** – large transfers (> R$ 1 000) require selfie + liveness detection.  
3. **Push Fraud Alerts** – powered by anomaly detection (gRPC API).

## 5. Troubleshooting Tips
- **Error 301:** Outdated app ➜ update and retry.  
- **Login Loop:** Clear app cache (Settings ▷ Storage) and relaunch.  
- **Face ID Fail:** Switch to password and re-enroll biometric.

## 6. Escalation Matrix
| Severity | Examples                        | Who to escalate to |
|----------|---------------------------------|--------------------|
| P1       | App outage, data breach         | SRE on-call        |
| P2       | Payments delayed > 2 h          | Payments Squad     |
| P3       | UI glitch, typo                 | Mobile Team JIRA   |

---

_Version 2.0 – 2025-04-22_
