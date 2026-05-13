# OSFI E-23 Compliance Checklist

An open-source checklist generator for OSFI E-23 model risk compliance. Built for Canadian banks, credit unions, and federally regulated lenders.

## What It Does

- Generates a comprehensive OSFI E-23 compliance checklist
- Maps each requirement to Saillent's five-tier governance framework
- Tracks completion status across model inventory, risk assessment, audit trails, governance, and training
- Exports audit-ready documentation

## Quick Start

git clone https://github.com/AlBochi/osfi-e23-checklist.git
cd osfi-e23-checklist
pip install -r requirements.txt
python generate.py --institution "Your Bank Name"

## Sample Output

| OSFI E-23 Section | Requirement | Status | Evidence |
|-------------------|-------------|--------|----------|
| 3.1 | Complete model inventory | Complete | inventory-2026-Q2.json |
| 3.2 | Risk classification framework | In Progress | risk-matrix-v2.pdf |
| 3.3 | Independent validation process | Not Started | - |
| 4.1 | Board oversight charter | Complete | board-charter-2026.pdf |

## Regulatory Alignment

- OSFI E-23 (full guideline coverage)
- FCAC Consumer Protection
- OPC Privacy Guidelines for AI

## Status

Proof of concept by Saillent.

## License

MIT
