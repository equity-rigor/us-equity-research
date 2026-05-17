# US Regulatory Desk

This file is the external regulatory environment reference for US-listed equities. Internal disclosure of regulatory exposure (FIN 48 reserves, CERCLA contingents, ASC 450 loss accruals) is handled by `forensic-accounting-checklist-us.md`; this file handles the regulators, the lists, the dockets, and the stage-of-action discipline that prevents the most common hallucination: confusing a lawmaker letter or a proposed rule with a formal designation.

Citation rule (D16): every regulatory designation cited as an investment-thesis anchor MUST resolve to an S1 source — the Federal Register notice, the agency's own published list, or the actual docket entry — with date and identifier. Press release alone is S3. Trade press alone is S5. Rumor is Pending and never anchors a headline.

Schema scope: every field in `schemas/memo.json` → `regulatory_status` is addressed below (`antitrust_open_matters`, `export_control_status`, `sector_regulator_open_matters`, `tariff_exposure_pct_cogs`, `tax_policy_exposures`). State-level and litigation are handled in their own sections though they wire into the same memo fields.

Stage-of-action discipline (universal): every regulatory action proceeds through stages. The single most common hallucination is collapsing stages into "X is regulated / blocked / sanctioned" when the actual state is "X has been requested for review by a lawmaker / proposed by an agency / preliminarily determined / consent-decree-negotiating." Always resolve to the specific stage and cite the document that establishes it.

---

## 1. Antitrust / Competition

### Regulators

- **FTC** — `https://www.ftc.gov` — federal civil antitrust + consumer protection; competition matters hub `https://www.ftc.gov/enforcement/competition-matters`; HSR premerger filings; consent decrees.
- **DOJ Antitrust Division** — `https://www.justice.gov/atr` — federal civil + criminal antitrust; merger reviews; case filings `https://www.justice.gov/atr/antitrust-case-filings-alpha`.
- **State AGs**: NY (`ag.ny.gov`), CA (`oag.ca.gov`), TX (`texasattorneygeneral.gov`), MA, WA. Increasingly active in tech antitrust; state AG coalitions can run parallel to or independent of federal action.
- **EU European Commission DG COMP** — `https://ec.europa.eu/competition/index_en.html` — Phase I (25 working days) → Phase II (90 working days, extendable). Decisions database searchable by case number `M.XXXXX`.
- **UK CMA** — `https://www.gov.uk/government/organisations/competition-and-markets-authority` — Phase 1 (40 working days) → Phase 2 (24 weeks). Post-Brexit, UK CMA reviews are independent of EU.
- **CCI India** — `https://www.cci.gov.in`.
- **Canada Competition Bureau** — `https://competitionbureau.canada.ca`.

### Stages (HSR premerger)

1. HSR filing accepted; initial 30-day waiting period begins.
2. Early termination granted OR waiting period expires (cleared).
3. **Second Request** issued — agency demands extensive documents/data; tolls the waiting period until substantial compliance. Signals deep review; ~3% of HSR filings receive Second Request.
4. Post-compliance 30-day review period.
5. Outcome: cleared / consent decree (with divestiture or conduct remedies) / litigation to block / abandoned by parties.

### Hallucination guards

- "M&A blocked" vs "Second Request issued" — Second Request is investigative escalation, NOT a block. Most Second Requests still resolve in clearance or consent decree.
- "FTC investigating" vs "FTC sued" — civil investigative demand (CID) is preliminary; complaint filing in federal district court or administrative court is the formal action.
- "EU CMA approved" — EU CMA does not exist. Either "EU European Commission cleared" or "UK CMA cleared." The delta matrix shorthand "EU CMA" refers to the European Commission DG COMP (not a body named "EU CMA"). Be explicit when writing the memo.
- Consent decree expiry: many tech-era consent orders (FTC v. Facebook 2012/2019/2024) have specific durations. Check the order, not the press release.

### Materiality threshold

In scope for `antitrust_open_matters` if: (a) Second Request issued, (b) consent decree under negotiation, (c) state AG complaint filed, (d) EU Commission Phase II opened, or (e) deal-pending and announced HSR clock running. NOT in scope: pure CID without formal complaint, "FTC reportedly considering" trade press only.

### S-tier mapping

- S1: court complaint docket entry on PACER; FTC/DOJ press release linked to filed complaint; EU Commission decision PDF; Federal Register consent order notice.
- S3: company 8-K Item 8.01 disclosing receipt of Second Request or CID.
- S5: legal alerts (Hogan Lovells, Cleary, Skadden, Sullivan & Cromwell, Wachtell).
- Pending: "people familiar" trade-press reports of agency interest with no docket.

### Example: AVGO

CFIUS + EU + UK + China SAMR scrutiny on major M&A is the modal pattern. The VMware close took 19 months, blocked-then-cleared-with-conditions across jurisdictions. Track each jurisdiction's stage separately; aggregate "approved" only means cleared everywhere required.

### Example: META

FTC consent order (2012, 2019 amended, 2024 proposed amendment), state AG antitrust complaints, EU DMA gatekeeper designation. Multiple parallel matters at different stages — memo must enumerate each, not collapse to "META has antitrust exposure."

---

## 2. Export Control & Sanctions

### Regulators and lists

- **BIS (Bureau of Industry and Security, Commerce)** — `https://www.bis.doc.gov`
  - **Entity List** — `https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list`. Most-cited list. Adds via Federal Register notice; each addition has a Fed Reg volume + page + date.
  - **Unverified List** (UVL) — parties BIS cannot verify; precursor to potential Entity List addition.
  - **Military End User (MEU) List** — separate list, separate license requirement.
  - **Validated End User (VEU)** — pre-approved end users in specified destinations; opposite signal of Entity List.
  - **Section 1758 emerging/foundational technology controls**.
  - **Foreign Direct Product Rule (FDPR)** — extraterritorial reach over items made anywhere using US-origin tech.
  - **End-User Affiliates Rule** — restrictions extend to affiliates with ≥50% ownership of listed entity.
- **OFAC (Treasury Office of Foreign Assets Control)** — `https://sanctionssearch.ofac.treasury.gov`
  - **SDN (Specially Designated Nationals) List** — comprehensive block.
  - **NS-CMIC (Non-SDN Chinese Military-Industrial Complex)** — investment prohibition on listed Chinese firms.
  - **Sectoral Sanctions Identifications (SSI) List** — narrower restrictions by sector (Russia financial, energy).
  - **Country programs** — Iran, North Korea, Cuba, Syria, Russia, Venezuela, Belarus.
  - Bulk download: `https://www.treasury.gov/ofac/downloads/sdn.xml`.
- **CFIUS (Committee on Foreign Investment in the United States, Treasury)** — `https://home.treasury.gov/policy-issues/international/the-committee-on-foreign-investment-in-the-united-states-cfius` — inbound FDI review of foreign acquisition of US businesses; mandatory filings for critical-tech, critical-infrastructure, sensitive-personal-data. Outcomes: cleared / mitigation agreement / forced divestiture / abandoned.
- **State Department DDTC (Directorate of Defense Trade Controls)** — `https://www.pmddtc.state.gov` — ITAR (International Traffic in Arms Regulations); USML (US Munitions List); separate from BIS EAR (Export Administration Regulations) for dual-use items.

### Stages (Entity List specifically)

1. Lawmaker letter requests addition (House/Senate committee chair, often China Select Committee). NOT a designation.
2. Inter-agency review begins (End-User Review Committee — ERC — comprises Commerce, State, Defense, Treasury, sometimes Energy).
3. ERC unanimous recommendation to add (or deny).
4. **Federal Register notice published** — formal addition takes effect. Specific volume / page / effective date.
5. License requirement triggered; existing inventory savings clause typically 30-60 days.
6. Removal / modification — also via Federal Register notice (extremely rare; typically requires demonstrating change in conduct).

### Hallucination guards

- "Designated" vs "lawmakers have requested" — single most-common research hallucination. A letter from a House committee chair urging addition to the Entity List is NOT a designation. It signals political pressure but no operational change. Always resolve to Federal Register publication.
- "Considering" vs "added" vs "proposed" — agency wording matters. The Federal Register notice is the operative event.
- Entity List addition of a parent does NOT automatically restrict every subsidiary unless the End-User Affiliates Rule applies (≥50% ownership) or the specific subsidiary is also listed. Verify entity-by-entity.
- OFAC SDN vs NS-CMIC — different restrictions. SDN is comprehensive block; NS-CMIC restricts US-person investment but not other transactions. Don't conflate.
- CFIUS "review opened" is not the same as "forced divestiture ordered." Mitigation agreements are common middle outcomes.

### Verification protocol

1. Identify the specific list (Entity / MEU / Unverified / SDN / NS-CMIC / SSI / CFIUS divestiture order).
2. Go to the government source directly. NOT the legal alert summary.
3. Capture: Federal Register volume + page + date + EAR §744 supplement reference for BIS additions; OFAC press release + SDN bulk file entry for OFAC.
4. If legal alert is the only entry point, cross-check ≥2 independent firms (Hogan Lovells, Crowell & Moring, Skadden, Arnold & Porter, Akin Gump) and resolve language ambiguity.

### Materiality threshold

In scope for `export_control_status` if company itself OR named subsidiary OR ≥10% customer/supplier is on any list, or CFIUS review is active on a pending transaction. Set boolean flag + `verified_as_of` date.

### S-tier mapping

- S1: Federal Register notice PDF; BIS Entity List page entry; OFAC SDN search returning hit; CFIUS annual report (lagged).
- S3: company 8-K disclosing receipt of Entity List addition impact or CFIUS mitigation agreement.
- S5: Reuters / WSJ / FT reports of inter-agency review.
- Pending: lawmaker letter, "considering" trade press.

### Example: NVDA

H100 / H200 / Blackwell licensing for China is gated by BIS performance thresholds under the October 2022 + October 2023 + 2024 rules; the H20 is the engineered-down China variant under those rules. Chinese hyperscaler customers (e.g., specific entities on the Entity List) face Entity List + End-User Affiliates restrictions. Memo must enumerate each China-related rule cycle distinctly with Federal Register cites, not lump as "NVDA China restrictions."

---

## 3. Trade & Tariffs

### Regulators

- **USTR (Office of the US Trade Representative)** — `https://ustr.gov` — Section 301 tariffs (currently the operative tool for China-origin imports); trade agreements; dispute resolution.
- **Commerce ITA (International Trade Administration)** — `https://www.trade.gov` — AD (antidumping) / CVD (countervailing duty) investigations; preliminary and final determinations.
- **USITC (US International Trade Commission)** — `https://www.usitc.gov` — Section 337 IP-based import investigations; AD/CVD injury determinations; HTS (Harmonized Tariff Schedule) maintenance.
- **CBP (Customs and Border Protection)** — `https://www.cbp.gov` — enforcement at the border; Withhold Release Orders under UFLPA (Uyghur Forced Labor Prevention Act); tariff classifications.

### Action types

- **Section 301** (Trade Act 1974) — unfair foreign trade practices; current China tariff regime (List 1/2/3/4A); modifications via USTR notice in Federal Register.
- **Section 232** (Trade Expansion Act 1962) — national security; steel/aluminum (2018, modified 2024-2025); auto investigations recurring.
- **Section 201** (Trade Act 1974) — global safeguards; rare (solar panels, washing machines historically).
- **AD/CVD** — antidumping / countervailing duty; product-specific, country-specific.

### Stages (AD/CVD)

1. Petition filed by domestic industry (or self-initiated by Commerce).
2. ITC preliminary injury determination (45 days).
3. Commerce preliminary AD/CVD determination (~140-160 days); duties begin to apply on entries.
4. Commerce final determination (~75 days later).
5. ITC final injury determination (~45 days later).
6. AD/CVD order published; duties enforced by CBP; subject to annual administrative review and 5-year sunset review.

### Hallucination guards

- "Tariff proposed" vs "tariff in effect" — Section 301 modifications go through public comment then USTR Federal Register notice. The notice specifies effective date.
- AD/CVD preliminary vs final — duties from prelim are subject to refund/adjustment after final. Magnitude shifts materially in the prelim-to-final transition.
- Exclusions: Section 301 had a USTR exclusion process; verify whether company's specific HTS codes are excluded (granular).

### Materiality threshold

`tariff_exposure_pct_cogs` is populated when import duties / tariff cost > 1% of COGS or otherwise disclosed by company as material. Source from 10-K MD&A discussion of tariff impact + import data.

### S-tier mapping

- S1: Federal Register USTR notice; Commerce IA decision memo on ITA docket; ITC decision on EDIS; CBP CSMS message.
- S3: company 10-K discussion of tariff exposure %, supply chain reshoring narrative on call.
- S5: trade press estimating sector-wide tariff impact.

---

## 4. Securities Enforcement & Investor Litigation

### Regulators and forums

- **SEC Division of Enforcement** — `https://www.sec.gov/divisions/enforce.shtml`
  - **Wells notice** — notification that staff intends to recommend an enforcement action; gives respondent opportunity for "Wells submission." Often disclosed by company in 8-K Item 8.01 if material.
  - **AAERs (Accounting and Auditing Enforcement Releases)** — `https://www.sec.gov/divisions/enforce/friactions.htm` — accounting fraud / disclosure cases; named individuals.
  - **Litigation releases** — `https://www.sec.gov/litigation/litreleases.htm` — every civil action filed by SEC.
  - **Administrative proceedings** vs **federal court litigation** — different forums, different evidentiary standards.
- **DOJ criminal** — parallel criminal proceedings; SEC civil + DOJ criminal frequently run in tandem on securities fraud / FCPA matters.
- **PCAOB (Public Company Accounting Oversight Board)** — `https://pcaobus.org`
  - Inspection reports of audit firms — searchable by firm `https://pcaobus.org/oversight/inspections/firm-inspection-reports`. Part I findings = audit failures.
  - Disciplinary orders against firms / individuals.
- **Rule 10b-5 federal class actions (Rule 23)** — securities fraud private actions. Tracked in Stanford Securities Class Action Clearinghouse `https://securities.stanford.edu`. PSLRA-governed pleading standard.
- **Delaware Chancery** — `https://courts.delaware.gov/chancery/` — fiduciary duty derivative suits; merger appraisal proceedings; deal litigation; books-and-records demands (DGCL §220).
- **Section 16(b) short-swing profits** — strict-liability disgorgement of insider trading profits within 6-month window.
- **PACER / RECAP** — federal docket access; PACER paid `https://pacer.uscourts.gov`, CourtListener free wrapper `https://www.courtlistener.com`.

### Stages (SEC enforcement)

1. Matter Under Inquiry (MUI) — informal staff inquiry. Rarely disclosed externally.
2. Formal Order of Investigation — SEC empowered to subpoena. May or may not be disclosed by company.
3. **Wells notice** — staff intends to recommend action. Often the first publicly-disclosed step in 8-K Item 8.01.
4. Wells submission by respondent.
5. Commission vote to authorize action.
6. Litigation filed (federal court) or AP instituted (administrative proceeding).
7. Settlement (consent without admission, or with neither-admit-nor-deny) OR trial.

### Hallucination guards

- "SEC investigating" vs "SEC sued" vs "SEC settled" — wildly different stages. Always cite the specific filing or release.
- Wells notice ≠ settlement / charge. ~30% of Wells notices result in no action.
- Restatement (8-K Item 4.02) does not automatically mean SEC enforcement, though it raises probability.
- Class action filing ≠ judgment. PSLRA dismissal rate is ~50%; many settle for nuisance value.

### Materiality threshold

In scope for memo's regulatory section if: SEC formal investigation disclosed (8-K 8.01 or 10-Q "Legal Proceedings"); Wells notice received; class action survived motion to dismiss; derivative suit certified; AAER published involving company; restatement that triggered Item 4.02.

### S-tier mapping

- S1: SEC litigation release; AAER; PCAOB disciplinary order; court docket entry; company 8-K disclosure with reference.
- S3: company press release / call discussion.
- S5: Bloomberg / Reuters reports of "ongoing SEC probe."

---

## 5. Sector Regulators

### FDA — `https://www.fda.gov`

- Dashboards: `https://dashboards.fda.gov`. Drug approvals: `https://www.accessdata.fda.gov/scripts/cder/daf/`. 510(k): `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm`. Adcom calendar: agency website.
- Action types: **IND** (Investigational New Drug) → **NDA** (New Drug Application — small molecule) / **BLA** (Biologics License) / **sNDA** (supplemental) → approval / **CRL** (Complete Response Letter — not an approval, identifies deficiencies, often resubmittable) / **Refuse-to-File** (deemed incomplete on submission). Devices: **510(k)** (substantially equivalent) / **PMA** (Premarket Approval — Class III).
- Recalls: Class I (reasonable probability of serious adverse health consequences / death) > Class II > Class III. Search `https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts`.
- Hallucination guards: **CRL is NOT a rejection** — it identifies deficiencies, often resolved with additional data and resubmission. PDUFA date is the target action date, not guaranteed; FDA can extend (3-month major-amendment clock reset). Adcom (advisory committee) vote is advisory; FDA can diverge.

### FCC — `https://www.fcc.gov`

- Docket search: `https://docs.fcc.gov`. Spectrum auctions: `https://www.fcc.gov/auctions`.
- Action types: **NPRM (Notice of Proposed Rulemaking)** — public comment; **R&O (Report & Order)** — final rule; **FNPRM** — further proposed rulemaking; **DA (Delegated Authority)** orders; **forbearance petitions**; license transfers (T-Mobile / Sprint precedent).
- Hallucination guards: NPRM is NOT a final rule. Spectrum auction "Phase 1" vs "winning bids" vs "license issued" are distinct stages.

### FERC — `https://www.ferc.gov`

- eLibrary docket search: `https://elibrary.ferc.gov`.
- Action types: order types include Section 203 (mergers/acquisitions), Section 205/206 (rate filings), pipeline certificates (NGA §7), LNG export authorizations, RTO/ISO market reforms. Order numbers: "Order No. 2222" (DER aggregation), "Order No. 1920" (transmission planning).

### NHTSA — `https://www.nhtsa.gov`

- Recalls portal: `https://www.nhtsa.gov/recalls`. ODI (Office of Defects Investigation) database.
- Stages: **ODI Preliminary Evaluation (PE)** → **Engineering Analysis (EA)** → **recall** (manufacturer-initiated or NHTSA-forced) → consent order possible.
- Recall classes (vehicle): defect / non-compliance. Population scope drives cost.
- Hallucination guards: PE is investigative, NOT a recall. A recall does not equal a fine. Tesla / autonomous-feature investigations have distinct cases (Autopilot vs FSD); cite the specific case ID.

### EPA — `https://www.epa.gov`

- Laws/regulations index: `https://www.epa.gov/laws-regulations`. ECHO enforcement: `https://echo.epa.gov`.
- Statutes: **CAA (Clean Air Act)** — NAAQS, mobile source standards, GHG endangerment finding; **CWA (Clean Water Act)** — NPDES permits; **RCRA (Resource Conservation and Recovery Act)** — solid/hazardous waste; **CERCLA / Superfund** — historic contamination, PRP designation drives `forensic-accounting-checklist-us.md` contingency analysis; **TSCA** — chemicals.

### FAA — `https://www.faa.gov`

- Action types: **type certificate** suspension / revocation; **Airworthiness Directives (ADs)**; production certificate restrictions (737 MAX precedent); operational restrictions.

### CFPB — `https://www.consumerfinance.gov`

- Enforcement actions: `https://www.consumerfinance.gov/enforcement/actions/`. Supervisory highlights.
- Action types: consent orders, civil money penalties, restitution; UDAAP (Unfair, Deceptive, or Abusive Acts or Practices) is the operative authority.

### OCC / FDIC / Federal Reserve banking supervision

- OCC: `https://www.occ.treas.gov` (national banks).
- FDIC: `https://www.fdic.gov` (state non-member banks; deposit insurance).
- Federal Reserve supervision: `https://www.federalreserve.gov/supervisionreg.htm` — BHCs; **CCAR / DFAST** annual stress test results (Fed-published table).
- Action types: **MOU (Memorandum of Understanding — informal)** → **consent order (formal, public)** → cease-and-desist → civil money penalty. CAMELS / CAMELS-O ratings (non-public).
- Hallucination guards: MOU is informal/often non-public. Consent order is public via OCC/FDIC enforcement database. Stress test "fail" vs "capital plan objected" vs "qualitative objection" are distinct.

### NRC — `https://www.nrc.gov`

- ADAMS docket: `https://adams.nrc.gov`. Action types: license amendments, civil penalties, operator licensing.

### USDA / FSIS — `https://www.usda.gov`

- FSIS recalls: `https://www.fsis.usda.gov/recalls`. Class I (high risk) / II / III. Plant inspection holds.

### HHS / CMS — `https://www.cms.gov`

- **NCD (National Coverage Determination)** — Medicare-wide; **LCD (Local Coverage Determination)** — MAC-by-MAC. Coverage decision is a major revenue catalyst for medical devices and certain drugs.
- Reimbursement cuts: physician fee schedule, IPPS / OPPS final rules in Federal Register annually.
- IRA Medicare drug price negotiation: CMS-published list of selected drugs, MFP (Maximum Fair Price) effective dates.

---

## 6. State-Level Regulation

US federalism means state regulators run parallel and sometimes ahead of federal action; the memo must enumerate state exposures, not lump as "regulatory risk."

- **California**
  - **CCPA / CPRA** (privacy) — California AG + CPPA enforce; private right of action limited to data-breach claims. `https://cppa.ca.gov`.
  - **CARB (Air Resources Board)** — vehicle emissions; ZEV mandate. `https://ww2.arb.ca.gov`. Often more stringent than federal EPA.
  - **Proposition 65** — chemical exposure warnings; private bounty enforcement creates plaintiff-bar risk.
  - **AB5** — independent contractor classification (gig economy: UBER, LYFT, DASH).
- **New York**
  - **DFS (Department of Financial Services)** — banks, insurers, virtual currency (BitLicense). `https://www.dfs.ny.gov`. Cybersecurity rule 23 NYCRR 500.
  - **NYAG (Attorney General)** — Martin Act gives broad securities-fraud authority (lower mens rea than federal 10b-5). Antitrust + consumer protection active.
- **Massachusetts**
  - **201 CMR 17** — data breach standard.
  - **AG Healey/Campbell** active in tech / consumer / pharma.
- **Texas**
  - **TX AG** active in antitrust (Google ad-tech case), tech regulation (HB 20 / HB 1181).
- **Delaware Chancery** — primary corporate-law venue for >65% of US public companies (DGCL incorporation); fiduciary-duty derivative suits, deal litigation, books-and-records (DGCL §220).

---

## 7. Tax Policy Exposures

Schema field `tax_policy_exposures` enumerates which regimes apply. Each named provision is verifiable in 10-K Income Taxes footnote (ASC 740). The IRS authority `https://www.irs.gov` issues guidance, revenue rulings, and proposed/final regulations through Federal Register.

- **BEAT (Base Erosion Anti-Abuse Tax)** — TCJA 2017 §59A. Applies to corps with ≥$500M gross receipts and base-erosion payments ≥3% of deductions. Look in 10-K tax rate reconciliation for "BEAT" line. Exposed: multinationals with material related-party outbound payments (royalties, services).
- **GILTI (Global Intangible Low-Taxed Income)** — §951A. CFC income inclusion at parent level. Affects nearly every US multinational with foreign subsidiaries; look for "GILTI" in tax reconciliation.
- **FDII (Foreign-Derived Intangible Income)** — §250 deduction (offsets GILTI). Preferential rate on US-export-driven IP income. Look for FDII deduction in tax reconciliation.
- **§174 R&D capitalization (TCJA 2017)** — post-2022 mandatory amortization of R&D over 5 years (US) / 15 years (foreign), replacing immediate expensing. **Material cash-tax headwind for R&D-intensive firms (semis, biotech, software).** Look for §174 disclosure in cash flow / tax footnote. Legislative repeal proposals have surfaced repeatedly; verify current statute, not 2017 form.
- **Pillar 2 / Global Minimum Tax (GMT 15%)** — OECD framework; UTPR / IIR mechanics. UK / EU / Japan / Korea / Canada in effect 2024-2025; US has NOT adopted IIR (CAMT is the partial domestic equivalent). Multinationals must compute country-by-country effective rate.
- **CAMT (Corporate Alternative Minimum Tax, 15%)** — IRA 2022; applies to corps with ≥$1B average AFSI (adjusted financial statement income) over 3 years. Treasury guidance ongoing.
- **Wayfair state sales tax nexus (2018)** — economic nexus replaced physical-presence test; affects e-commerce and remote service providers.
- **IRA §45X Advanced Manufacturing Production Credit** — clean energy components (solar, wind, batteries); per-unit credit. Verify in 10-K subsidy / credit footnote.
- **IRA §48 Investment Tax Credit** — clean energy investment.
- **CHIPS Act §48D Advanced Manufacturing Investment Credit** — 25% of qualified semis manufacturing investment. Affects INTC, MU, TSM US fab, GFS, ON, TXN, TER.
- **§41 R&D Credit** — long-standing, non-refundable; interacts with §174 capitalization (timing not amount).
- **NOL carryforward** — TCJA limits post-2017 NOLs to 80% of taxable income; indefinite carryforward; §382 limits on change-of-control.

### Verification

10-K Note "Income Taxes" must reconcile statutory 21% to effective rate by named adjustment. Cross-check tax-policy exposure claims against this reconciliation; if a regime is not visible there, it is unlikely material.

### Example: MRK pharma

GILTI + FDII + Pillar 2 all relevant; biotech R&D-intensive so §174 capitalization affects cash tax; CMS IRA drug negotiation is the larger near-term policy driver and lives in §5 (HHS/CMS).

---

## 8. Litigation

Beyond SEC enforcement (§4):

- **Federal class actions (Rule 23)** — securities fraud (10b-5), antitrust (Sherman §1/§2, Clayton §7), product liability, consumer (state UDAP claims aggregated), data breach. Tracked: Stanford SCAC for securities; Bloomberg Law / Lex Machina for others.
- **Derivative suits** — typically Delaware Chancery or federal court; demand-futility or pre-suit-demand discipline; books-and-records (DGCL §220) often precedes filed derivative.
- **Delaware Chancery deal litigation** — fiduciary duty in M&A; *Revlon*, *Unocal*, entire-fairness review; appraisal proceedings (DGCL §262).
- **ITC §337 import bans** — for tech IP, can be faster and more potent than district-court patent litigation. EDIS docket `https://www.usitc.gov/secretary/edis.htm`. Stages: complaint → investigation instituted → ALJ initial determination → Commission review → potentially limited / general exclusion order.
- **Patent litigation (district court)** — PACER + Lex Machina (premium) for IP analytics; RPX `https://www.rpxcorp.com` for tracking.
- **Product liability MDL (multidistrict litigation)** — JPML docket; consolidated for discovery; bellwether trials; settlement matrices.

### Hallucination guards

- Class action filed ≠ certified ≠ settled. Settlement value depends on certification, merits posture, damages model.
- ITC exclusion order takes 12-18 months to issue; "ITC complaint filed" is opening salvo.
- Delaware Chancery appraisal is rare-but-real downside in M&A; affects deal economics, not always disclosed by acquirer.

---

## Closing — relationship to forensic-accounting-checklist-us.md

This file covers the **external** regulatory environment: who regulates, what they do, which stage actions are at, how to avoid stage-collapse hallucinations. The complementary file `forensic-accounting-checklist-us.md` covers the **internal** accounting disclosure of regulatory exposure: ASC 450 loss-contingency accruals, FIN 48 / ASC 740 uncertain-tax-position reserves, CERCLA / environmental remediation accruals on the balance sheet, contingent litigation liabilities in the Commitments & Contingencies footnote, Form 8-K Item 8.01 disclosures of regulatory events. When the memo cites "$X reserve for matter Y" that is forensic-side; when it cites "matter Y is at Second Request stage with DOJ" that is this file.

Both files wire into the same `regulatory_status` block in `schemas/memo.json` — this file populates the qualitative stage / agency / status fields; the forensic file populates the dollar exposure fields where disclosed.
