#!/usr/bin/env python3
"""
Saillent OSFI E-23 Compliance Scoring Matrix (CSM-1)
Quantifies compliance maturity across all OSFI E-23 domains
using weighted scoring, gap severity analysis, and regulatory timeline projections.
"""

import json
import math
from datetime import datetime, timedelta
from collections import defaultdict

class OSFIComplianceScorer:
    """
    Saillent Compliance Scoring Matrix (CSM-1)
    Maps OSFI E-23 requirements to quantifiable maturity levels
    with projected regulatory examination readiness dates.
    """
    
    MATURITY_LEVELS = {
        1: {"label": "Initial", "description": "Ad hoc or undocumented processes", "score_range": (0, 20)},
        2: {"label": "Developing", "description": "Processes documented but inconsistently applied", "score_range": (21, 40)},
        3: {"label": "Defined", "description": "Standardized processes with ownership assigned", "score_range": (41, 60)},
        4: {"label": "Managed", "description": "Quantitative metrics tracked and reviewed", "score_range": (61, 80)},
        5: {"label": "Optimizing", "description": "Continuous improvement with automation", "score_range": (81, 100)}
    }
    
    OSFI_DOMAINS = {
        "Governance & Oversight": {"weight": 0.25, "max_score": 100},
        "Model Inventory & Classification": {"weight": 0.20, "max_score": 100},
        "Risk Assessment & Validation": {"weight": 0.25, "max_score": 100},
        "Monitoring & Audit Trails": {"weight": 0.15, "max_score": 100},
        "Training & Culture": {"weight": 0.15, "max_score": 100}
    }
    
    def __init__(self, institution_name):
        self.institution = institution_name
        self.domain_scores = {}
        self.findings = []
        self.remediation_items = []
    
    def score_domain(self, domain, current_score, target_score=85, notes=""):
        """Score a single OSFI E-23 domain."""
        if domain not in self.OSFI_DOMAINS:
            raise ValueError(f"Unknown domain: {domain}")
        
        maturity = self._get_maturity(current_score)
        target_maturity = self._get_maturity(target_score)
        gap = target_score - current_score
        
        # Calculate projected remediation timeline
        if gap <= 0:
            timeline_days = 0
            priority = "MAINTAIN"
        elif gap <= 15:
            timeline_days = 30
            priority = "LOW"
        elif gap <= 30:
            timeline_days = 90
            priority = "MEDIUM"
        elif gap <= 50:
            timeline_days = 180
            priority = "HIGH"
        else:
            timeline_days = 365
            priority = "CRITICAL"
        
        projected_date = (datetime.now() + timedelta(days=timeline_days)).strftime("%Y-%m-%d")
        
        self.domain_scores[domain] = {
            "current_score": current_score,
            "target_score": target_score,
            "gap": gap,
            "current_maturity": maturity["label"],
            "target_maturity": target_maturity["label"],
            "weight": self.OSFI_DOMAINS[domain]["weight"],
            "weighted_score": round(current_score * self.OSFI_DOMAINS[domain]["weight"], 2),
            "priority": priority,
            "projected_remediation_date": projected_date,
            "notes": notes
        }
        
        if gap > 0:
            self.findings.append({
                "domain": domain,
                "severity": priority,
                "gap": gap,
                "current": maturity["label"],
                "target": target_maturity["label"],
                "timeline_days": timeline_days
            })
    
    def _get_maturity(self, score):
        for level, data in self.MATURITY_LEVELS.items():
            low, high = data["score_range"]
            if low <= score <= high:
                return data
        return self.MATURITY_LEVELS[5]
    
    def calculate_overall_score(self):
        """Calculate weighted overall compliance score."""
        total_weighted = sum(d["weighted_score"] for d in self.domain_scores.values())
        max_possible = sum(d["weight"] * d.get("target_score", 100) for d in self.domain_scores.values())
        
        # Find maximum possible weighted score
        total_weight = sum(self.OSFI_DOMAINS[d]["weight"] for d in self.domain_scores)
        
        overall = total_weighted / total_weight if total_weight > 0 else 0
        
        return {
            "overall_compliance_score": round(overall, 2),
            "overall_maturity": self._get_maturity(overall)["label"],
            "total_domains_assessed": len(self.domain_scores),
            "domains_at_target": sum(1 for d in self.domain_scores.values() if d["gap"] <= 0),
            "critical_gaps": sum(1 for f in self.findings if f["severity"] == "CRITICAL"),
            "estimated_full_compliance": self._calculate_full_compliance_date()
        }
    
    def _calculate_full_compliance_date(self):
        """Calculate projected date for full OSFI E-23 compliance."""
        if not self.findings:
            return "Already compliant"
        
        max_days = max(f["timeline_days"] for f in self.findings)
        return (datetime.now() + timedelta(days=max_days)).strftime("%Y-%m-%d")
    
    def generate_scoring_report(self, filepath):
        """Generate complete compliance scoring report."""
        overall = self.calculate_overall_score()
        
        report = {
            "report_type": "Saillent OSFI E-23 Compliance Scoring Report",
            "framework": "CSM-1 (Compliance Scoring Matrix v1.0)",
            "institution": self.institution,
            "generated_at": datetime.now().isoformat(),
            "overall_compliance": overall,
            "domain_scores": self.domain_scores,
            "findings": sorted(self.findings, key=lambda x: x["gap"], reverse=True),
            "regulatory_timeline": {
                "next_examination_risk": "HIGH" if overall["overall_compliance_score"] < 60 else "MEDIUM" if overall["overall_compliance_score"] < 80 else "LOW",
                "estimated_full_compliance": overall["estimated_full_compliance"],
                "recommended_review_cadence": "Quarterly" if overall["overall_compliance_score"] < 70 else "Semi-annual"
            },
            "saillent_recommendations": []
        }
        
        # Generate recommendations
        for finding in report["findings"]:
            report["saillent_recommendations"].append({
                "domain": finding["domain"],
                "priority": finding["severity"],
                "action": f"Engage Saillent Tier {self._map_domain_to_tier(finding['domain'])} services for {finding['domain'].lower()} remediation",
                "expected_improvement": f"+{finding['gap']} points within {finding['timeline_days']} days"
            })
        
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _map_domain_to_tier(self, domain):
        mapping = {
            "Governance & Oversight": 4,
            "Model Inventory & Classification": 1,
            "Risk Assessment & Validation": 2,
            "Monitoring & Audit Trails": 3,
            "Training & Culture": 5
        }
        return mapping.get(domain, 1)

if __name__ == "__main__":
    print("Saillent Compliance Scoring Matrix (CSM-1)")
    print("=" * 55)
    
    scorer = OSFIComplianceScorer("Confidential Canadian Bank")
    
    scorer.score_domain("Governance & Oversight", 72, 85, "Board policy in place. Committee charter needs updating.")
    scorer.score_domain("Model Inventory & Classification", 55, 90, "Shadow AI detection not yet implemented. 5 unregistered models found.")
    scorer.score_domain("Risk Assessment & Validation", 48, 85, "Independent validation program incomplete. Only 60% of high-risk models validated.")
    scorer.score_domain("Monitoring & Audit Trails", 38, 80, "Real-time monitoring not deployed. Manual audit trail processes.")
    scorer.score_domain("Training & Culture", 65, 80, "Role-based training program exists but completion rate at 70%.")
    
    report = scorer.generate_scoring_report("osfi_scoring_report.json")
    
    overall = report["overall_compliance"]
    print(f"\n📊 OSFI E-23 Compliance Scoring Report")
    print(f"   Institution: {report['institution']}")
    print(f"   Overall Score: {overall['overall_compliance_score']}%")
    print(f"   Maturity Level: {overall['overall_maturity']}")
    print(f"   Domains at Target: {overall['domains_at_target']}/{overall['total_domains_assessed']}")
    print(f"   Critical Gaps: {overall['critical_gaps']}")
    print(f"   Est. Full Compliance: {overall['estimated_full_compliance']}")
    
    print(f"\n📋 Domain Breakdown:")
    for domain, scores in report["domain_scores"].items():
        bar = "█" * int(scores["current_score"] / 10) + "░" * (10 - int(scores["current_score"] / 10))
        print(f"   {bar} {domain}: {scores['current_score']}% → Target: {scores['target_score']}% [{scores['priority']}]")
    
    print(f"\n📋 Top Remediation Priorities:")
    for rec in report["saillent_recommendations"][:3]:
        print(f"   [{rec['priority']}] {rec['action']}")
