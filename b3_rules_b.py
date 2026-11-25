# -*- coding: utf-8 -*-
"""B.3 curated rules, part B (B.3.2.5 to B.3.2.12.1). Source: BSC 2027 ICE Rulebook v1.0, pp.21-29."""

B3_RULES_B = [
{
 "id": "B.3.2.5", "title": "LC – Lateral Cross Member", "page": 21, "kind": "requirement", "priority": "High",
 "components": ["Lateral Cross Members", "ALC", "BLC", "CLC", "DLC", "ELC", "FLC", "GLC", "RLC"],
 "body": [
  "Lateral cross members (LC) shall not be less than 203.5 mm (8 in) long. LCs shall not have a bend; however, they may be part of a bent system, provided the minimum length is met between bend tangents. LCs are denoted by the points they connect (e.g. ALC, FLC, etc.). The cross members which connect the left and right points A, B, C, D, F and E/G for ‘Nose’ vehicles (in which case DLC may be omitted) shall be made of primary materials. The LC at Point R for Rear FAB systems may be secondary material and must meet the minimum length described above.",
  "Note: RLC exists only with complete Rear Bracing per B.3.2.13.2"
 ],
 "plain": [
  "A lateral cross member must be at least 203.5 mm (8 in) long.",
  "An LC may not be bent, but it may be part of a bent system if the minimum length is met between the bend tangents.",
  "LCs are named by the points they connect: ALC, BLC, CLC, DLC, ELC, FLC, GLC, RLC.",
  "The LCs that connect left and right points A, B, C, D, F and E/G (for nose vehicles, where DLC may be omitted) must be Primary material.",
  "The RLC at Point R for rear FAB systems may be Secondary material, but must still meet the minimum length.",
  "RLC exists only when complete Rear Bracing per B.3.2.13.2 is present."
 ],
 "engineering": [
  "'Length' means the tube length between its terminating joints measured on the centreline, not the vehicle track width. Check the straight segment between bend tangents if the LC is part of a bent system.",
  "Material classification is node-based. Build the member schedule with the node names so the material callout follows the rule: ALC/BLC/CLC/DLC/ELC/FLC/GLC at the listed nodes are Primary; RLC can be Secondary.",
  "Do not add an RLC to a frame that does not have complete rear bracing — it is not a required member in that configuration and adds weight without a defined load path."
 ],
 "notes": ["Figure B-12 shows the LC locations; the note under the figure is reproduced above."]
},
{
 "id": "B.3.2.6", "title": "RRH – Roll Hoop Members", "page": 22, "kind": "requirement", "priority": "High",
 "components": ["RRH", "ALC", "BLC", "RHO", "LDB"],
 "body": [
  "The RRH is a planar structure behind the driver’s back and defines the boundary between the front-half (fore) and rear-half (aft) of the roll cage. The driver and seat must be entirely forward of this plane. The RRH shall be inclined between 0 and 20° from vertical as viewed from the side of the vehicle. The minimum width of the RRH is 736 mm (29 in), centred on the seat, at a point 686 mm (27 in) seat bottom.",
  "The vertical members of the RRH may be straight or bent and are defined as beginning at Point A at the lower end and terminating at Point B at the upper end shown in Figure B-12. The vertical members shall be continuous from Point A to B (i.e. not multiple segments joined by welding). The vertical members shall be joined by Lateral Crossmembers ALC and BLC at the bottom and top for the RRH. ALC and BLC members must be continuous tubes or adhere to B.3.2.14 - Butt Joints.",
  "Points AR/AL, at the lower end of the RRH vertical members, are defined as the intersection with the LFS and ALC.",
  "Points BR/BL are defined as the uppermost end of the RRH vertical members. For Roll Cages constructed with bends at the upper end of the vertical members, Point B occurs at the uppermost tangent of the bend. Point B is the intersection of the RRH vertical members with the RHO and BLC. Point B may not reside on the bend or a linear distance from the end of the bend.",
  "Note: ALC, BLC, RRH members, LDB and the shoulder belt tube shall all be coplanar."
 ],
 "plain": [
  "The RRH is a flat (planar) structure behind the driver's back and marks the boundary between the front and rear halves of the cage. The driver and seat must be entirely forward of that plane.",
  "Seen from the side, the RRH must lean between 0° and 20° from vertical.",
  "The minimum RRH width is 736 mm (29 in), centred on the seat, measured 686 mm (27 in) above the seat bottom. (The printed rule says 'at a point 686 mm (27 in) seat bottom' — the word 'above' appears to be missing; see the ambiguity note.)",
  "The RRH vertical members may be straight or bent. They start at Point A and end at Point B, and must be continuous — not multiple pieces welded together.",
  "The verticals are joined at the bottom and top by ALC and BLC. ALC and BLC must be continuous tubes or follow the butt-joint rules in B.3.2.14.",
  "AR/AL are where the RRH verticals intersect the LFS and ALC. BR/BL are the uppermost ends of the verticals. If the top is bent, Point B is at the uppermost tangent of the bend, not on the bend and not a linear distance from the end of the bend.",
  "ALC, BLC, RRH members, LDB and the shoulder-belt tube must all lie in the same plane."
 ],
 "engineering": [
  "The RRH is the primary rollover and seatback structure and the datum for most cage geometry. Keep it planar in the front view; any out-of-plane offset at a node introduces eccentricity into the rollover load path.",
  "The 0–20° inclination is measured in side view from true vertical. A more laid-back RRH improves driver room but consumes rear-bracing space and reduces the effective height of the B points.",
  "Build the 736 mm × 686 mm template as a CAD plane: create a plane 686 mm above the seat bottom, measure the RRH centrelines at that height, and confirm the width is ≥736 mm and centred on the seat (equal left/right offsets).",
  "Point B is a tangent point. If you place B on the bend arc, you shorten the effective vertical member and can fail the template. Check B at the uppermost tangent and confirm the RHO/BLC intersection is at that point.",
  "The coplanarity note is critical: if the LDB or shoulder-belt tube is out of the RRH plane, the seatback and belt loads become eccentric and the RRH is loaded in torsion."
 ],
 "notes": [
  "Source ambiguity: 'at a point 686 mm (27 in) seat bottom' is missing a word, read as '686 mm above the seat bottom'. The figure B-13 dimension (685.800 mm) supports this reading. Confirm with BTC if the measurement basis is challenged.",
  "Formatting artefact normalised: 'Figure B- 12' → 'Figure B-12'."
 ]
},
{
 "id": "B.3.2.7", "title": "LDB – Lateral Diagonal Bracing", "page": 23, "kind": "requirement", "priority": "High",
 "components": ["LDB", "RRH"],
 "body": [
  "The RRH must be diagonally braced. The diagonal brace(s) must extend from one RRH vertical member to the other. The top and bottom intersections of the LDB members and the RRH vertical members must be no more than 127 mm (5 in) from points A and B. The angle between the LDB members and the RRH vertical members must be greater than or equal to 20°. Lateral bracing may consist of more than one member.",
  "A single straight LDB is exempt from the maximum length in B.3.2.1 - Member Requirements."
 ],
 "plain": [
  "The RRH must be diagonally braced from one RRH vertical to the other.",
  "The top and bottom intersections of the LDB and the RRH verticals must be no more than 127 mm (5 in) from Points A and B.",
  "The angle between the LDB and the RRH vertical must be at least 20°.",
  "More than one LDB member is allowed.",
  "A single straight LDB is exempt from the maximum length rule in B.3.2.1."
 ],
 "engineering": [
  "The 127 mm tolerance lets the brace land near the node without intersecting exactly at A/B. Measure the straight-line distance from each intersection to the theoretical node, not along the tube.",
  "The ≥20° angle is measured in the RRH plane (front view), not in 3D. If you use an X-brace, each diagonal must independently meet the 20° and 127 mm rules.",
  "The length exemption applies only to a single straight LDB. A bent or multi-piece LDB is subject to B.3.2.1 and B.3.2.4.",
  "A shallow LDB angle gives poor triangulation: the brace carries mostly axial load but the joint at A/B sees high local bending. Keep the angle as large as packaging allows."
 ],
 "notes": [
  "Figure B-14 includes dimensions printed as '736.600 mm' and '685.800 mm' in the source; the extracted text shows '736.600 mm 68 5. 80 0 m m'. Refer to the page image for the authoritative figure dimensions."
 ]
},
{
 "id": "B.3.2.8", "title": "RHO – Roll Hoop Overhead Members", "page": 24, "kind": "requirement", "priority": "High",
 "components": ["RHO", "RRH", "CLC", "BLC", "FBM"],
 "body": [
  "The aft (rearward) ends of the RHO members intersect the RRH within 50.8 mm (2 in) of Points BR and BL (defined by BLC). The forward ends of the RHO members, or the start of the bend between RHO and FBM define points CR and CL (Figure B-12). CLC, BLC and RHO members must all be coplanar. Out-of-plane bends at the aft (rearward) ends of the RHO members are not permitted. When a bend is used at Point CR/CL or BR/BL these points are defined at the start of the bend on the top-most plane of the Roll Cage, shown in Figure B-16: Roll Cage, Template Installation. When a bend is used at Point C, CLC must attach at or between the tangents of the bend but shall not be further aft of the start of the bend.",
  "The ends of the BLC define the location of points BL and BR. For vehicles constructed with bends at the top of the RRH, point B shall be on the inside end of the bend. Point B may not reside on the bend or a linear distance from the end of the bend.",
  "Points CR and CL must be between at least 304.8 mm (12 in) forward of a point, in the vehicle’s side view, defined by the intersection of the RHO members and a vertical line rising from the aft end of the seat bottom. This point on the seat is defined by the seat bottom intersection with a 101.6 mm (4 in) radius circle which touches the seat bottom and the seat back. The top edge of the template is exactly horizontal with respect to gravity.",
  "Points CR and CL and Points BR and BL must also be no lower than the top edge of the template, 1041.4 mm (41 in) above the seat and shall satisfy the Lateral Space requirements in Rule B.3.3.1 - Lateral Space.",
  "Note: The top, longitudinal edge of the template shall be oriented exactly horizontal with respect to gravity."
 ],
 "plain": [
  "The rear ends of the RHO must meet the RRH within 50.8 mm (2 in) of BR and BL (which are defined by the BLC).",
  "The forward ends of the RHO — or the start of the bend between RHO and FBM — define CR and CL.",
  "CLC, BLC and RHO must be coplanar. Out-of-plane bends at the rear ends of the RHO are not allowed.",
  "If a bend is used at CR/CL or BR/BL, those points are at the start of the bend on the top-most plane of the cage.",
  "If a bend is used at Point C, the CLC must attach at or between the bend tangents and may not be further aft than the start of the bend.",
  "The BLC ends define BL and BR. If the RRH top is bent, Point B is on the inside end of the bend; B may not be on the bend or a linear distance from the end of the bend.",
  "CR and CL must be at least 304.8 mm (12 in) forward of the seat reference point: the point where the RHO intersects a vertical line rising from the aft end of the seat bottom. The seat point is where the seat bottom meets a 101.6 mm (4 in) radius circle that touches the seat bottom and seat back.",
  "CR/CL and BR/BL must be no lower than the top edge of the template, 1041.4 mm (41 in) above the seat, and must satisfy the lateral-space rule B.3.3.1.",
  "The top longitudinal edge of the template must be exactly horizontal."
 ],
 "engineering": [
  "The RHO is the roof structure and defines the driver's head clearance. Build the template as a CAD solid: a 101.6 mm radius circle tangent to the seat bottom and seat back, a vertical line from the aft seat-bottom tangent, a top edge 1041.4 mm above the seat, and the top edge horizontal.",
  "CR/CL must be at least 304.8 mm forward of that vertical line and at least 1041.4 mm above the seat. The phrase 'between at least 304.8 mm forward' is awkward; treat 304.8 mm as a minimum forward offset and flag any design that relies on a different reading.",
  "The 'top-most plane' matters when measuring B and C at bend tangents. Use the same plane for the template and for the node definitions, otherwise the 1041.4 mm check is inconsistent.",
  "Out-of-plane bends at the rear of the RHO create a kink in the rollover load path and are explicitly prohibited. If the RHO transitions to the FBM out of plane, re-route the tube rather than bending it at the rear node."
 ],
 "notes": [
  "Source ambiguity: 'Points CR and CL must be between at least 304.8 mm (12 in) forward of a point' — 'between at least' is not grammatical. The likely intent is a minimum forward offset of 304.8 mm. Flag for BTC clarification.",
  "Formatting artefact normalised: 'Figure B-12).CLC' → 'Figure B-12). CLC'."
 ]
},
{
 "id": "B.3.2.8.1", "title": "Gussets for Lateral Clearance", "page": 25, "kind": "requirement", "priority": "Medium",
 "components": ["Gussets", "RHO", "RRH", "SIM", "FBM"],
 "body": [
  "Gussets may be added between the RHO and RRH to satisfy the requirements of Rule B.3.3.1 - Lateral Space. The added tubes shall be of primary material (B.3.2.16 - Roll Cage Materials). Gusset tubes connecting the SIM to RRH or FBM for the purposes of satisfying the requirements of Rule B.3.3.1 - Lateral Space shall be of secondary material (B.3.2.3 - Secondary Members and Tubes. Gussets shall not interfere with the minimum radial clearance required around the fire extinguisher pull knob (B.8.8.5 - Location and Clearance). Tubes governed by this Rule are not subject to bend angle limits in B.3.2.1 - Member Requirements and B.3.2.4 - Additional Support Tubes."
 ],
 "plain": [
  "Gussets may be added between the RHO and RRH to meet the lateral-clearance rule B.3.3.1. Those added tubes must be Primary material.",
  "Gusset tubes connecting the SIM to the RRH or FBM for lateral clearance must be Secondary material.",
  "Gussets must not interfere with the minimum radial clearance around the fire-extinguisher pull knob (B.8.8.5).",
  "Tubes governed by this rule are exempt from the bend-angle limits in B.3.2.1 and B.3.2.4."
 ],
 "engineering": [
  "This is an exception clause. Gussets used purely to satisfy lateral clearance can ignore the 30° bend limit and the support-tube length rules, but they still must be welded all around and must meet the material class.",
  "Do not use the exception to bypass the Primary/Secondary split: RHO↔RRH gussets are Primary; SIM↔RRH/FBM gussets are Secondary. The material callout follows the joint, not the word 'gusset'.",
  "Check the extinguisher knob clearance in the cockpit before finalising gusset placement. A gusset that satisfies lateral space but blocks the pull knob is still non-compliant."
 ],
 "notes": [
  "Formatting artefact: the source has '(B.3.2.3 - Secondary Members and Tubes.' without a closing parenthesis; closing parenthesis supplied for readability."
 ]
},
{
 "id": "B.3.2.9", "title": "LFS – Lower Frame Side Members", "page": 26, "kind": "requirement", "priority": "High",
 "components": ["LFS", "RRH", "FLC", "ELC"],
 "body": [
  "The Lower Frame Side (LFS) members define the lower right and left edges of the roll cage. These members are joined to the bottom of the RRH at Point A and extend generally forward, to Point F, at least as far forward of every driver’s heel when seated in a normal driving position and actuating the pedals to their full extents. The forward ends of the LFS members are joined by a lateral cross member, FLC (Figure B-11). The intersection of the LFS members and the FLC define the points FR and FL. In ‘Nose’ designs, as shown in Figure B-18, the LFS shall extend forward to Point E, and is joined by lateral cross members FLC and ELC (Figure B-11). Alternative ‘Nose’ designs are feasible wherein Points E and F are co-located, provided adequate foot protection is achieved."
 ],
 "plain": [
  "The LFS members form the lower left and right edges of the cage. They join the bottom of the RRH at Point A and run forward to Point F — at least as far forward as every driver's heel when seated normally and pushing the pedals to full travel.",
  "The forward ends of the LFS are joined by the FLC. That intersection defines FR and FL.",
  "On a 'Nose' design, the LFS extends forward to Point E and is joined by both the FLC and the ELC.",
  "An alternative nose design may put E and F at the same point, provided adequate foot protection is achieved."
 ],
 "engineering": [
  "The LFS is the lower load path and the datum for the driver's feet. The heel check is a worst-case anthropometric check: use the tallest/longest-legged driver, seat in the driving position, pedals at full travel (brake, clutch, throttle), and measure the heel envelope against Point F.",
  "The FLC and ELC nodes define the front structure. If E and F are co-located, the foot protection must be shown to be equivalent — do not assume that deleting the ELC is acceptable without the toe structure of B.3.2.10.",
  "Keep the LFS straight where possible; any bend must meet B.3.2.1 and may require support under B.3.2.4."
 ],
 "notes": [
  "Cross-reference inconsistency: the rule says 'as shown in Figure B-18', but Figure B-18 is 'Roll Cage, Gussets'. The LFS nose example is Figure B-19. Treat the reference as likely intended Figure B-19."
 ]
},
{
 "id": "B.3.2.10", "title": "SIM – Side Impact Members", "page": 27, "kind": "requirement", "priority": "High",
 "components": ["SIM", "RRH", "FBM", "DLC", "GLC", "LFS"],
 "body": [
  "The two Side Impact Members (SIM) define a horizontal mid-plane within the roll cage. These members are joined to the RRH, defining Point S, and extend forward, to a point at least as far forward of every driver’s toes when seated in a normal driving position. The forward ends of the SIM members shall intersect with the FBM, defining Points DR and DL, this intersection shall be joined by a lateral crossmember, DLC. The SIM members must be between 203 mm (8 in) and 356 mm (14 in) above the inside seat bottom (Figure B-15) at all positions between points S and D. In ‘Nose’ designs, as shown in Figure B-19, the SIM extends forward to Points GR and GL, which shall be joined by a lateral cross member, GLC (Figure B-11). In this case, DLC may be omitted if GLC provides adequate protection for the driver’s toes as noted below.",
  "The feet of any driver must be entirely behind the plane defined by points FR/FL and DR/DL. In nose designs the driver’s feet must be entirely behind the plane defined by points GR/GL and ER/EL and below the plane defined by GR/GL and DR/DL.",
  "In any design, the structure should provide 25.4 mm (1 in) of clearance between a straight edge applied to any two points on the roll cage and any part of the driver’s foot while actuating all pedals through the full range of motion (See B.7.1.1 - Brake Pedal), If there is insufficient clearance, then an additional structure of secondary material shall be constructed between FBM, SIM and LC members above the driver’s toes when viewed from both the front and side."
 ],
 "plain": [
  "The two SIMs define a horizontal mid-plane in the cage. They join the RRH at Point S and run forward at least as far as every driver's toes when seated normally.",
  "The forward ends of the SIM intersect the FBM at DR and DL; that intersection is joined by the DLC.",
  "The SIM must be between 203 mm (8 in) and 356 mm (14 in) above the inside seat bottom at all positions between S and D.",
  "On a nose design, the SIM extends to GR and GL, joined by the GLC. The DLC may be omitted if the GLC gives adequate toe protection.",
  "The driver's feet must be entirely behind the plane FR/FL–DR/DL. On a nose design they must also be behind GR/GL–ER/EL and below GR/GL–DR/DL.",
  "In any design, the structure should give 25.4 mm (1 in) clearance between a straight edge applied to any two cage points and any part of the driver's foot through full pedal travel (see B.7.1.1). If clearance is insufficient, add secondary structure between the FBM, SIM and LC above the toes when viewed from the front and side."
 ],
 "engineering": [
  "SIM height is a band, not a single dimension. Measure at every station between S and D, including bend tangents and the as-built node locations. A SIM that slopes out of the band anywhere between S and D fails.",
  "The 25.4 mm foot clearance is a straight-edge (convex-hull) test, not a point-to-point distance. Sweep a straight edge between any two cage points and check the driver's foot envelope through full pedal travel.",
  "The toe-protection structure is required when the clearance is not inherent. It must be Secondary material and must sit above the toes when viewed from both the front and the side — a single front hoop is not sufficient.",
  "The SIM is classified Secondary for material purposes but carries the side-impact load. Design the joints at S, D and the DLC for the side load, not just the cage weight."
 ],
 "notes": [
  "Normative wording: 'the structure should provide 25.4 mm' uses 'should' (recommendation), while the following clause 'shall be constructed' is mandatory if clearance is insufficient. Treat 25.4 mm as the design target and the added structure as mandatory when it is not met.",
  "Formatting artefact: 'motion (See B.7.1.1 - Brake Pedal), If there is' has a capital 'If' after a comma; reproduced as printed."
 ]
},
{
 "id": "B.3.2.11", "title": "UST – Under Seat Tubes", "page": 27, "kind": "requirement", "priority": "High",
 "components": ["UST", "LFS", "Driver Restraint"],
 "body": [
  "A secondary tube, or system of secondary tubes, shall pass underneath the seat, positioned in such a way to prevent the driver from passing through the plane of the LFS in the event of seat failure. The UST system shall connect to the LFS members on both sides of the roll cage.",
  "The UST may also serve as the mounting location for the seat and/or the anti-submarine belts per B.4.5.3 - Seat Mounting Points and B.4.2.6.3 - Anti Submarine Belt Attachment."
 ],
 "plain": [
  "A secondary tube or tube system must pass under the seat. It must stop the driver from passing through the LFS plane if the seat fails.",
  "The UST must connect to the LFS on both sides of the cage.",
  "It may also be used to mount the seat and/or the anti-submarine belts (B.4.5.3 and B.4.2.6.3)."
 ],
 "engineering": [
  "The UST is an anti-submarining and seat-failure catch, not just a seat bracket. A single-sided or bracket-only connection is non-compliant: it must tie into both LFS members.",
  "If the UST carries belt loads, the load path must go into the UST and LFS, not into the seat shell. Check the belt attachment points against B.4.2.6.3 and the seat mounts against B.4.5.3.",
  "Keep the UST low enough to catch the driver but clear of the seat adjustment range and the driver's hips."
 ],
 "notes": []
},
{
 "id": "B.3.2.12", "title": "FBM – Front Bracing Members", "page": 28, "kind": "requirement", "priority": "High",
 "components": ["FBM", "RHO", "SIM", "LFS"],
 "body": [
  "Front Bracing Members shall join the RHO, SIM and LFS (Figure B-21) at Points C, D and F respectively. The upper Front Bracing Members (FBMUP) shall join Point C on the RHO to Point D on the SIM. It is preferred to notch the SIM around the FBM. The lower Front Bracing Members (FBMLOW) must join point D to point F. The FBMUP and FBMLOW shall each be continuous tubes. The angle between the FBMUP and the vertical must be less than or equal to 45°. If Front FAB, per Rule B.3.2.13.1 - Front Bracing, is used there is no angle requirement between FBM and vertical."
 ],
 "plain": [
  "The FBMs join the RHO, SIM and LFS at Points C, D and F.",
  "The upper FBM (FBMUP) joins C on the RHO to D on the SIM. Notching the SIM around the FBM is preferred.",
  "The lower FBM (FBMLOW) must join D to F.",
  "FBMUP and FBMLOW must each be continuous tubes.",
  "The angle between the FBMUP and vertical must be 45° or less.",
  "If Front FAB per B.3.2.13.1 is used, there is no angle requirement between the FBM and vertical."
 ],
 "engineering": [
  "'Continuous' means one tube from node to node, with splices only if they comply with B.3.2.14. A joint in the FBMUP at mid-height is a common inspection failure.",
  "The 45° limit is measured in side view between the FBMUP centreline and true vertical. A steeper FBMUP is more efficient in compression but may interfere with driver egress and the template.",
  "The Front FAB exception removes the angle limit because the FAB carries the load — but only if the complete front-bracing system (P and Q nodes) is built. A partial front brace does not qualify.",
  "Notching the SIM around the FBM is a recommendation. If you notch, maintain the SIM wall and re-check the net section at the notch."
 ],
 "notes": ["Normative wording: 'It is preferred to notch the SIM around the FBM' is a recommendation, not a mandatory requirement."]
},
{
 "id": "B.3.2.12.1", "title": "Gussets for RHO and FBM", "page": 29, "kind": "requirement", "priority": "High",
 "components": ["Gussets", "RHO", "FBM"],
 "body": [
  "If the RHO and FBM on one side of the vehicle are not comprised jointly of one tube, bent at point C, then a gusset is required at point C to support the joint between the RHO and the FBM. The total weld length of the gusset must be two times the tubing circumference (of the primary material). Thus, if a tube is used to brace the FBM and RHO, it must be primary material. Plate gussets may be used if the thickness of the material meets or exceeds that of the primary material used."
 ],
 "plain": [
  "If the RHO and FBM on one side are not one continuous tube bent at Point C, a gusset is required at C to support the joint.",
  "The total weld length of the gusset must be two times the tubing circumference of the Primary material.",
  "If a tube is used to brace the FBM and RHO, it must be Primary material.",
  "Plate gussets are allowed if the plate thickness meets or exceeds the Primary material thickness."
 ],
 "engineering": [
  "This is a node-reinforcement rule. Calculate the total weld length around the gusset-to-tube contact (both sides for a tube gusset) and compare it with 2 × π × D of the Primary tube.",
  "A plate gusset must be at least as thick as the Primary tube wall. This is a direct thickness comparison, not an equivalent-strength calculation — do not substitute a thinner high-strength plate.",
  "If the RHO and FBM are one continuous bent tube through C, no gusset is required. Document the tube continuity in the CAD member schedule so the inspector can see why the gusset is absent."
 ],
 "notes": ["Formatting artefact: 'Figure B-23: RHO / FBM Gussets.' is printed twice in the source; one caption retained."]
}
]
