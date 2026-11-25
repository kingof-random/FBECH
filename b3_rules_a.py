# -*- coding: utf-8 -*-
"""B.3 curated rules, part A (B.3.1 to B.3.2.4). Official wording transcribed from the
BAJA SAEINDIA Chennai 2027 ICE Rulebook v1.0, PDF pp.17-20. PDF line-break hyphenation
artefacts are normalised; wording is otherwise unchanged. 'plain' and 'engineering' are
FEROX interpretation layers, not official wording."""

B3_RULES_A = [
{
 "id": "B.3.1", "title": "Objective", "page": 17, "kind": "requirement", "priority": "High",
 "components": ["Roll Cage — General"],
 "body": [
  "The purpose of the roll cage is to maintain a minimum space surrounding the driver. The cage must be designed and fabricated to prevent any failure of the cage’s integrity during normal operation or during a collision or roll over."
 ],
 "plain": [
  "The roll cage exists to keep a minimum survival space around the driver.",
  "It must not fail — in normal driving, in a collision, or in a rollover. Every detailed rule in B.3 serves this objective."
 ],
 "engineering": [
  "Treat B.3.1 as the governing performance intent behind every dimensional rule in Article 3. A cage that satisfies each individual dimension but compromises the driver's survival space is still non-compliant.",
  "Design and check the load paths for the worst cases: vertical (rollover), longitudinal (front and rear impact), lateral (side impact), and local footwell intrusion. The objective is the fallback test an inspector can apply when a detail is ambiguous."
 ],
 "notes": []
},
{
 "id": "B.3.2", "title": "Roll Cage Structure", "page": 17, "kind": "requirement", "priority": "High",
 "components": ["Roll Cage — General", "Welding & Fabrication"],
 "body": [
  "The roll cage must be a space frame of tubular steel. The following section outlines the requirements of the physical members and joining methods of the roll cage. Roll cage and Frame Members must be fully welded, and welds must not be ground, sanded or modified so as to prevent inspection. Roll Cage Members and tubes shall not exhibit cutouts, notches, wrinkles, kinks, or any detrimental deformation to the cross-section. Roll cage members and tubes shall be joined by welding the entire circumference and shall not exhibit any injurious defects such as cracking, burn-through, cold lapping, or insufficient penetration.",
  "Terminology used in the Rule book relating to the roll cage structure is given below:",
  "Frame: The entire tubular structure including required members and non-cantilevered tubes.",
  "Roll Cage: Primary and Secondary Members used to protect the driver.",
  "Tube: A Primary or Secondary element, which is not required to begin and end at Named Points, except where noted.",
  "Member: A Primary or Secondary required element beginning and ending at Named Points.",
  "Named Point: The intersection of the centrelines of two or more joining members."
 ],
 "plain": [
  "The cage must be a welded, tubular-steel space frame.",
  "All roll cage and frame members must be fully welded. Welds may not be ground, sanded or otherwise modified in a way that prevents inspection.",
  "No member or tube may have cut-outs, notches, wrinkles, kinks, or any harmful deformation of its cross-section.",
  "Joints must be welded around the entire circumference and must be free of cracking, burn-through, cold lap, and insufficient penetration.",
  "The rule defines five terms used throughout Article 3: Frame, Roll Cage, Tube, Member and Named Point. A Named Point is where the centrelines of two or more joining members intersect."
 ],
 "engineering": [
  "Build the cage as a centreline wireframe in CAD. All rule dimensions are centreline-to-centreline, so the outer surface model is not the measurement datum.",
  "The Member/Tube distinction matters: Members must begin and end at Named Points; Tubes generally need not. Several rules exempt Tubes from Named Point termination, so misclassifying a member can silently change which rules apply.",
  "'Fully welded' and 'entire circumference' mean no stitch welding or partial penetration on structural joints. Weld dressing is acceptable only to the extent that it does not hide the weld from inspection — do not grind a weld flush and then paint over it.",
  "Plan weld access before the cage is assembled. Joints that cannot be welded all around after assembly must be sequenced or re-detailed."
 ],
 "notes": []
},
{
 "id": "B.3.2.1", "title": "Member Requirements", "page": 17, "kind": "requirement", "priority": "High",
 "components": ["Roll Cage — General", "LFS", "SIM", "FAB"],
 "body": [
  "Roll cage members shall be made of steel tube and may be straight or bent. Straight members may not extend longer than 1016 mm (40 in) between Named Points. Members exceeding this length shall comply with Rule B.3.2.4 - Additional Support Members. Bent members shall not contain an individual bend greater than 30°. that does not occur at a Named Point; and may not extend longer than 838 mm (33 in) between Named Points or comply with Rule B.3.2.4 - Additional Support Members. Small bend radii (<152 mm or 6 in) that terminate at Named Points are expected, and are not considered to make a member bent, regardless of angle. A bend that terminates at a Named Point implies the point lies at or between the points of tangency of the bend, as shown in Figure B-6. Required dimensions between roll cage members are defined by measurements between member centrelines, except where noted.",
  "Junctions of Primary and Secondary members described below must be within 50.8 mm (2 in) of the Named Point, except where noted.",
  "Mitred tubing joints of greater than 5° shall be treated as bends. Mitres of less than 5° shall be treated as butt joints and subject to Rule B.3.2.14 - Butt Joints. Required members constructed of multiple members, such as the SIM and LFS, shall be judged as continuous members from Named Point to Named Point, except where noted."
 ],
 "plain": [
  "Members must be steel tube and may be straight or bent.",
  "Straight member: maximum 1016 mm (40 in) between Named Points. If longer, it must follow the Additional Support rules in B.3.2.4.",
  "Bent member: no individual bend greater than 30°, and maximum 838 mm (33 in) between Named Points, unless it follows B.3.2.4.",
  "Small bend radii (under 152 mm / 6 in) that terminate at a Named Point are expected and do not make a member 'bent', regardless of angle. The Named Point lies at or between the bend's tangent points.",
  "All dimensions are measured between member centrelines unless a rule says otherwise.",
  "Junctions between Primary and Secondary members must be within 50.8 mm (2 in) of the Named Point, unless noted.",
  "A mitred joint greater than 5° counts as a bend. A mitre under 5° counts as a butt joint and must follow B.3.2.14.",
  "Multi-piece required members such as the SIM and LFS are judged as continuous from Named Point to Named Point."
 ],
 "engineering": [
  "Model every straight segment against 1016 mm and every bent segment against both 30° per bend and 838 mm between Named Points. Check the actual centreline geometry after all bends, not the nominal tube length before bending.",
  "The 50.8 mm junction tolerance is a fabrication tolerance, not permission to move a node. Keep the weld intersection within 50.8 mm of the theoretical Named Point and re-check every dependent dimension (SIM height, LDB angle, FBM angle, lateral clearance) at the as-built node location.",
  "A bend that terminates at a Named Point is defined by its tangent points. Putting the node at the arc apex instead of the tangent changes the effective member length and can push a bend over the 30° or 838 mm limit.",
  "Mitres greater than 5° consume the bend-angle budget and length limits; mitres under 5° must be sleeved as butt joints. Choose the joint type deliberately rather than letting the fabrication process decide."
 ],
 "notes": [
  "Source ambiguity: the printed sentence reads 'Bent members shall not contain an individual bend greater than 30°. that does not occur at a Named Point; and may not extend longer than 838 mm ...'. The clause 'that does not occur at a Named Point' is grammatically detached. It is unclear whether the 30° limit applies to all bends or only bends away from a Named Point. FEROX design baseline: apply the stricter reading (no individual bend > 30° anywhere) and raise a rules inquiry to BTC if a bend at a Named Point must exceed 30°."
 ]
},
{
 "id": "B.3.2.2", "title": "Primary Members", "page": 18, "kind": "definition", "priority": "High",
 "components": ["RRH", "RHO", "FBM", "Lateral Cross Members", "LFS", "Gussets"],
 "body": [
  "The required members of the roll cage are illustrated in Figure B-7 and Figure B-8. Members shall always begin and end at Named Points. Tubes, where required, are not required to terminate at Named Points except where noted. Primary members and tubes shall conform to B.3.2.16 - Roll Cage Materials.",
  "Primary members are:",
  "• RRH: Rear Roll Hoop Members",
  "• RHO: Roll Hoop Overhead Members",
  "• FBM: Front Bracing Members (Upper, Lower, and Lower when present)",
  "• ALC: Aft Lateral Cross Member",
  "• BLC: Overhead Lateral Cross Member",
  "• CLC: Upper Lateral Cross Member",
  "• DLC: SIM Lateral Cross Member",
  "• ELC: Nose SIM Lateral Cross Member (When Present)",
  "• FLC: Front Lateral Cross Member",
  "• GLC: Nose Front Lateral Cross Member (When Present)",
  "• LFS: Lower Frame Side Members",
  "Primary Tubes Are:",
  "• B.3.2.8.1 - Gussets for Lateral Clearance",
  "• B.3.2.12.1 - Gussets for RHO and FBM",
  "• B.3.2.10 - Additional Structure for Driver Toe Protection"
 ],
 "plain": [
  "This is the official list of Primary members: RRH, RHO, FBM, ALC, BLC, CLC, DLC, ELC (when present), FLC, GLC (when present) and LFS.",
  "Members must always begin and end at Named Points. Tubes that are required do not have to terminate at Named Points unless a rule says so.",
  "All Primary members and tubes must meet the material rules in B.3.2.16.",
  "Three items are classified as Primary Tubes: the B.3.2.8.1 lateral-clearance gussets, the B.3.2.12.1 RHO/FBM gussets, and the B.3.2.10 additional toe-protection structure."
 ],
 "engineering": [
  "The list is exhaustive for the 'Primary' designation. If a member is not on this list and does not qualify under one of the Primary Tube clauses, treat it as Secondary and apply B.3.2.3.",
  "The distinction drives material selection, wall thickness, and which members may carry the cage loads. Do not label a member 'primary' in CAD unless it is on this list or covered by B.3.2.8.1 / B.3.2.12.1 / B.3.2.10.",
  "The FBM entry is ambiguous: 'Upper, Lower, and Lower when present' repeats 'Lower'. Check the intended configuration (upper and lower FBM, with the lower member only on certain layouts) before finalising the member schedule."
 ],
 "notes": [
  "Source ambiguity: 'FBM: Front Bracing Members (Upper, Lower, and Lower when present)' repeats 'Lower'. Likely intended 'Upper, Lower, and Upper when present' or 'Upper and Lower when present'; the printed text is unclear. Flag for BTC clarification.",
  "Cross-reference ambiguity: B.3.2.10 is titled 'SIM – Side Impact Members' but is listed here as 'Additional Structure for Driver Toe Protection'. The toe-protection clause is the final paragraph of B.3.2.10; the listing is correct in substance but the title mismatch is a source inconsistency."
 ]
},
{
 "id": "B.3.2.3", "title": "Secondary Members and Tubes", "page": 19, "kind": "requirement", "priority": "High",
 "components": ["LDB", "SIM", "FAB", "Lateral Cross Members", "UST", "Gussets"],
 "body": [
  "Secondary members and tubes shall be of tubular steel, having a minimum wall thickness of 0.89 mm (0.035 in) and a minimum outside diameter of 25.4 mm (1 in) or rectangular steel tubes having a minimum wall thickness of 0.89 mm (0.035 in) and a minimum outside dimension of 25.4 mm (1 in).",
  "Secondary members are:",
  "• LDB: Lateral Diagonal Bracing Member(s)",
  "• SIM: Side Impact Members",
  "• FAB: Fore/Aft Bracing Members",
  "• RLC: Rear Lateral Cross Member",
  "Secondary tubes are:",
  "• B.3.2.11 - Under Seat Tube (UST)",
  "• B.3.2.4 - Additional Support Tubes",
  "• B.3.2.8.1 - Gussets for Lateral Clearance",
  "• B.4.2 - Any tube used to mount safety belts",
  "• B.6.5.1 - Any tube used to mount the fuel tank",
  "• B.6.5 - Any tube used to protect the fuel system."
 ],
 "plain": [
  "Secondary members and tubes must be tubular steel with a minimum wall of 0.89 mm (0.035 in) and a minimum outside diameter of 25.4 mm (1 in). Rectangular steel tube is allowed with the same minimum wall and a minimum outside dimension of 25.4 mm (1 in).",
  "Secondary members are LDB, SIM, FAB and RLC.",
  "Secondary tubes include the UST, Additional Support Tubes, lateral-clearance gussets, and any tube used to mount safety belts, mount the fuel tank, or protect the fuel system."
 ],
 "engineering": [
  "These are absolute minimums. Do not assume 4130 or DOM is required for secondary members — the rule only requires tubular steel at the stated minimums. Verify wall thickness with a micrometer at several points away from welds and use the minimum measured value.",
  "SIM and FAB are designated Secondary even though they are major structural members. That is a material-class designation, not a statement that they are lightly loaded; design them for the side-impact and longitudinal load paths.",
  "The list pulls in B.4.2, B.6.5 and B.6.5.1 from other articles. Resolve those cross-references before releasing the member schedule."
 ],
 "notes": []
},
{
 "id": "B.3.2.4", "title": "Additional Support Tubes", "page": 20, "kind": "requirement", "priority": "High",
 "components": ["Roll Cage — General", "FAB", "SIM", "LDB"],
 "body": [
  "For bent or straight Primary Roll Cage Members that exceed the maximum allowable length, Additional Support Tubes shall be added. For straight members, a single secondary tube shall connect from the mid-point (+/-127 mm or 5 in) to a Named Point. For bent members, a single secondary tube shall connect from between the tangents of the bend to a Named Point. If Additional Support Tubes are used, the supported Roll Cage Member shall be re-evaluated for length between Named Points and the location of the Additional Support Tube. Primary bent members shall not have a bend greater than 30°.",
  "For bent or straight Secondary Roll Cage Members that exceed the maximum allowable length or bend angle, Additional Support Tubes shall be added. For members that exceed only the allowable length OR the allowable bend angle, a single Additional Support Tube is required, with one end connected as described above and the other shall terminate within 2” of a Named Point. For members that exceed both the length AND bend angle limits, two Additional Support Tubes shall connect from between the tangents of the bend to two unique Named Points.",
  "Note: As an exception to the definition of Tube in B.3.2.2 – Primary Members and Tubes, Additional Support Tubes shall have one end terminate at a Named Point."
 ],
 "plain": [
  "If a Primary member is too long, add an Additional Support Tube.",
  "Straight Primary member: one secondary tube from the midpoint, within ±127 mm (5 in), to a Named Point.",
  "Bent Primary member: one secondary tube from between the bend tangents to a Named Point.",
  "After adding support, re-check the supported member's length between Named Points and the support location. A bent Primary member still may not have a bend greater than 30°.",
  "Secondary members that exceed the length or bend limits follow the Figure B-9 table: one support if only one limit is exceeded (one end as described above, the other within 2 in of a Named Point); two supports to two unique Named Points if both limits are exceeded.",
  "Additional Support Tubes are an exception to the Tube definition: one end must terminate at a Named Point."
 ],
 "engineering": [
  "Figure B-9 is a lookup table, not a judgment call. Read the member's length band and bend angle band, then provide the stated number of supports at the stated location.",
  "A support tube is only effective if it lands at a Named Point (or within 2 in for the secondary case). Landing it mid-span of another tube adds a bending load to that tube without creating a proper node.",
  "The ±127 mm midpoint tolerance allows the support to land near a convenient node. After choosing the support point, re-run the length check on each resulting sub-span and check the support tube's own slenderness.",
  "Weld the support tube around its full circumference at both ends. It is a structural member even though it is a 'tube' under the terminology."
 ],
 "notes": [
  "Figure B-9 is reproduced in this rule's detail panel and in the Support Finder tool. The table applies to SECONDARY MEMBERS ONLY.",
  "The 2 in (50.8 mm) termination tolerance appears in the source with a typographic double-quote character; it is reproduced as 50.8 mm in the checks."
 ],
 "table": {
  "caption": "Figure B-9: Table of Secondary member support",
  "columns": ["Length → / Bend Angle ↓", "≤ 838 mm (33 in)", "> 838 mm (33 in) & < 1016 mm (40 in)", "> 1016 mm (40 in)"],
  "rows": [
   ["0°", "No Supports Required", "No Supports Required", "1 Support Member Required*"],
   ["≤ 30°", "No Supports Required", "1 Support Member Required**", "1 Support Member Required**"],
   ["> 30°", "1 Support Member Required**", "2 Support Members Required**", "2 Support Members Required**"]
  ],
  "notes": ["* Required within 50.8 mm (2 in) of the midpoint of the overall tube length", "** Required within the tangents of the bend"]
 }
}
]
