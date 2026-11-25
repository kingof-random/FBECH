# -*- coding: utf-8 -*-
"""B.3 curated rules, part C (B.3.2.13 to B.3.7.3). Source: BSC 2027 ICE Rulebook v1.0, pp.29-36."""

B3_RULES_C = [
{
 "id": "B.3.2.13", "title": "FAB – Fore - Aft Bracing", "page": 29, "kind": "requirement", "priority": "High",
 "components": ["FAB", "RRH", "RHO"],
 "body": [
  "The RRH shall be restrained from rotation and bending in the side view by a system of triangulated bracing. Triangulation angles (projected to the side view) must be at least 20° between members. Bracing shall either be front bracing or rear bracing (FAB), a better design shall result if both front and rear bracing are incorporated:",
  "Rear Bracing - directly restrain both Points B from longitudinal displacement in the event of failure of the joints at Points C; or",
  "Front Bracing - restrain both Points C from longitudinal and vertical displacement, thus supporting Points B through the RHO members."
 ],
 "plain": [
  "The RRH must be restrained from rotation and bending in side view by triangulated bracing.",
  "The triangulation angle, projected into side view, must be at least 20° between members.",
  "Bracing must be either front bracing or rear bracing (FAB). A better design uses both.",
  "Rear bracing directly restrains both B points from longitudinal displacement if the joints at C fail.",
  "Front bracing restrains both C points from longitudinal and vertical displacement, supporting B through the RHO."
 ],
 "engineering": [
  "FAB is the cage's side-view shear system. Without it the RRH is a portal frame with no shear stiffness; the 20° minimum is what makes the triangle effective.",
  "Measure the angle in the side projection between the bracing members (or between the brace and the RRH/RHO). Do not measure the 3D angle.",
  "Choose front, rear, or both based on packaging and the load path. If both are used, each system must independently satisfy its own rules; they are not averaged."
 ],
 "notes": ["Normative wording: 'a better design shall result if both front and rear bracing are incorporated' is a recommendation, not a requirement."]
},
{
 "id": "B.3.2.13.1", "title": "Front Bracing", "page": 29, "kind": "requirement", "priority": "High",
 "components": ["FAB", "FBM", "SIM", "LFS"],
 "body": [
  "Front Bracing systems shall connect the FBMUP to the SIM, on the same sides. The intersection with the FBMUP members shall be within 127 mm (5 in) measured as a straight-line distance from centreline to centreline of Point C. The intersection with the SIM members defines Point P which shall be vertically supported by further members extending from Point P to the LFS members, which defines Point Q. Points P and Q exist only with complete Front Bracing."
 ],
 "plain": [
  "Front bracing connects the FBMUP to the SIM on the same side.",
  "The intersection with the FBMUP must be within 127 mm (5 in), measured straight-line from centreline to centreline, of Point C.",
  "The intersection with the SIM defines Point P. P must be vertically supported by members running down to the LFS, defining Point Q.",
  "P and Q exist only with complete Front Bracing."
 ],
 "engineering": [
  "The front brace is a knee from the FBMUP down to the SIM, plus a vertical post from P to Q on the LFS. Both are needed for a complete front-bracing system.",
  "The 127 mm is a straight-line distance in 3D from the C node to the brace/FBMUP intersection. Measure centreline to centreline, not edge to edge.",
  "Do not label P and Q on a frame that lacks the P–Q member. The nodes are defined by the complete system, not by the drawing."
 ],
 "notes": []
},
{
 "id": "B.3.2.13.2", "title": "Rear Bracing", "page": 29, "kind": "requirement", "priority": "High",
 "components": ["FAB", "RRH", "RLC", "ALC"],
 "body": [
  "Rear Bracing systems shall create a structural triangle, in the side view, on each side of the vehicle. Each triangle shall be aft of the RRH, include the RRH as a vertical element, have one vertex at Point B, and one vertex at either Point S or Point A. The members forming this structural triangle shall be continuous and comply with Rule B.3.2.1. The third vertex is the intersection of these two continuous members and is joined by a Rear Lateral Crossmember (RLC) defining Point R which shall additionally be connected to Point S or A, whichever is not part of the structural triangle. This additional connection, which is required for a complete FAB system, and is not subject to B.3.2.1 - Member Requirements and may be formed using multiple joined members and may encompass a bend of greater than 30°.",
  "Attachment of rear FAB system shall be within 50.8 mm (2 in) of Point B, Point S and Point A, on each side of the vehicle. Members connecting to Point A shall attach at an angle of 45° or greater as measured from the ALC. Distances are measured in a straight-line from centreline to centreline of the tube intersections. The aft vertex of each rear bracing triangle defines Point R and shall be joined by a Lateral Crossmember, RLC, per B.3.2.5 - LC – Lateral Cross Member."
 ],
 "plain": [
  "Rear bracing must create a structural triangle in side view on each side of the vehicle.",
  "Each triangle must be aft of the RRH, include the RRH as the vertical element, have one vertex at B and one at S or A.",
  "The triangle members must be continuous and comply with B.3.2.1.",
  "The third vertex is where those two continuous members meet. It is joined by the RLC, which defines Point R. R must also connect to S or A — whichever is not in the triangle.",
  "That additional connection is required for a complete FAB system. It is not subject to B.3.2.1, may be made of multiple joined members, and may include a bend greater than 30°.",
  "The rear FAB attachments must be within 50.8 mm (2 in) of B, S and A on each side.",
  "Members connecting to A must attach at 45° or greater measured from the ALC.",
  "Distances are straight-line, centreline to centreline. The aft vertex defines R and is joined by an RLC per B.3.2.5."
 ],
 "engineering": [
  "The rear triangle is the primary rear rollover and side-impact load path. Keep the triangle vertices at B and S (or A) and the third vertex aft of the RRH; a triangle that is not aft of the RRH does not restrain the RRH.",
  "The 50.8 mm attachment tolerance applies at all three nodes. Check each node independently.",
  "The ≥45° angle at A is measured from the ALC (the lateral cross member), not from the LFS. A near-vertical FAB attachment at A is required; a shallow attachment puts the ALC in bending.",
  "The R-to-S/A tie is the 'complete FAB' qualifier. Without it, the triangle is not a complete system. The exception allowing bends >30° applies only to that additional connection, not to the triangle members."
 ],
 "notes": []
},
{
 "id": "B.3.2.14", "title": "Butt Joints", "page": 30, "kind": "parent", "priority": "Medium",
 "components": ["Butt Joints", "Roll Cage — General"],
 "body": [],
 "plain": ["This is a parent heading. The requirements are in B.3.2.14.1 (Requirement), B.3.2.14.2 (Size) and B.3.2.14.3 (Welding)."],
 "engineering": ["Read all three subsections together: a butt joint needs a sleeve (14.1), the sleeve has a minimum size and wall (14.2), and the weld has a minimum configuration (14.3)."],
 "notes": ["B.3.2.14 has no body text in the source; the requirements are carried by its subsections."]
},
{
 "id": "B.3.2.14.1", "title": "Requirement", "page": 30, "kind": "requirement", "priority": "High",
 "components": ["Butt Joints"],
 "body": [
  "Many roll cage members are required to be continuous tubes and may not be made of multiple pieces. Roll cage members which are made of multiple tubes, joined by welding in a butt joint, shall be reinforced with an internal sleeve. Tubes which are joined at an angle greater than 5° need not be sleeved; angles of less than 5° shall be considered butt joints."
 ],
 "plain": [
  "Many cage members must be continuous tubes and may not be made of multiple pieces.",
  "If a member is made of multiple tubes joined by a butt weld, it must have an internal sleeve.",
  "Joints at an angle greater than 5° do not need a sleeve; angles under 5° are treated as butt joints."
 ],
 "engineering": [
  "The 5° threshold separates a true butt joint (sleeve required) from an angled joint (no sleeve). This is counterintuitive: a slight kink under 5° is treated as a butt joint and must be sleeved, while a larger angle is treated as a bend/fish-mouth joint.",
  "Measure the included angle between tube centrelines at the joint. Document the angle in the weld map so the inspector can see why a joint is or is not sleeved."
 ],
 "notes": []
},
{
 "id": "B.3.2.14.2", "title": "Size", "page": 30, "kind": "requirement", "priority": "High",
 "components": ["Butt Joints"],
 "body": [
  "Sleeves shall be designed to fit tightly inside the joint being reinforced. External sleeves are not allowed. Sleeves shall extend into each side of the butt joint, a length of at least two times the diameter of the tubes being reinforced and shall be made from steel at least as thick as the tubes being reinforced."
 ],
 "plain": [
  "Sleeves must fit tightly inside the joint being reinforced.",
  "External sleeves are not allowed.",
  "A sleeve must extend at least two tube diameters into each side of the butt joint.",
  "The sleeve must be steel at least as thick as the tube it reinforces."
 ],
 "engineering": [
  "Internal sleeve length ≥ 4D total (2D each side of the joint). Wall thickness ≥ tube wall. 'Tightly' means no gap; a loose sleeve is not effective and is an inspection failure.",
  "External sleeves (wrap-around fishplates) are explicitly prohibited — do not design one as a repair.",
  "For a round tube, check the sleeve OD against the tube ID after allowing for the tube's actual wall tolerance; a sleeve that is too tight will not assemble, one that is too loose will not carry load."
 ],
 "notes": []
},
{
 "id": "B.3.2.14.3", "title": "Welding", "page": 31, "kind": "requirement", "priority": "High",
 "components": ["Butt Joints", "Welding & Fabrication"],
 "body": [
  "The general arrangement of an acceptable sleeved joint is shown in Figure B-25. A butt weld and four (4) rosette welds are required. Two (2) rosette welds are required on each tube piece. Rosette welds are to be made in holes of a minimum diameter of 15.9 mm (0.625 in).",
  "A minimum of 101.6 mm (4 in) of linear weld is required to secure the sleeve inside the joint, including the butt joint and the rosette welds."
 ],
 "plain": [
  "A sleeved joint needs a butt weld plus four rosette welds — two on each tube piece.",
  "Rosette holes must be at least 15.9 mm (0.625 in) diameter.",
  "At least 101.6 mm (4 in) of total linear weld is required to secure the sleeve, counting the butt weld and the rosette welds."
 ],
 "engineering": [
  "The 101.6 mm is the total linear weld around the joint (butt weld + rosette welds), not per side. Count it on the finished joint, not on the drawing.",
  "Rosette holes 15.9 mm minimum must be drilled in the outer tube over the sleeve and then welded. Two holes per tube piece, spaced around the circumference.",
  "Sequence: fit sleeve, tack, weld butt, drill rosettes, weld rosettes, inspect. Grinding the welds flush is not permitted if it prevents inspection (B.3.2)."
 ],
 "notes": []
},
{
 "id": "B.3.2.15", "title": "Welding Process Check", "page": 31, "kind": "requirement", "priority": "High",
 "components": ["Welding & Fabrication", "Weld Samples"],
 "body": [
  "Prior to welding any joint on any of the vehicle’s roll cage elements, each person shall individually complete two welding samples, defined below, using the same primary materials and processes as used in the roll cage element welds. All welding samples shall be submitted at TI. Vehicles for which complete sets of welding samples are not submitted, or for which any of the welding samples are judged inadequate, shall not be allowed to compete in dynamic or endurance events.",
  "Welding samples shall be made from the same tube material, diameter, and thickness as the welds made by each person on the primary roll cage elements. For information on best practices for weld samples, see www.bajasae.net/go/downloads.",
  "All weld samples shall be indelibly marked, by permanent means such as engraving, etching, or stamping with all the following information:",
  "• School Name or School Initials",
  "• Welder Name or Welder Initials",
  "• Date of construction of weld sample",
  "Sample 1 – Destructive Testing: The sample shall comprise a 90° joint, the leg length of which is unrestricted shall be (Figure B-26) be destructively tested. Passing samples shall exhibit a joint failure in the base material and not in the weld metal. The testing method is free and either tensile or bending failure may be induced; however, the peak stress must be located at the weld. In the case of bending failure, take care that the largest bending moment is located at the weld. Samples shall be tested prior to arrival at competition, and both pieces presented for inspection in the case of complete separation during testing.",
  "Sample 2 – Destructive Inspection The sample shall comprise of two tubes joined at a 30° angle with a length of at least 149.86 mm (5.9 in) from the centre of the joint (Figure B-27) to the end of each extended leg, and at least 50.8 mm (2 in) on the closed end of the joint. The sample shall be sectioned along the length of tube to reveal adequate and uniform weld penetration (Figure B-27). Samples shall be tested prior to arrival at competition, and both pieces presented for inspection in the case of complete separation during testing."
 ],
 "plain": [
  "Before welding any roll cage joint, each person must individually complete two weld samples using the same Primary materials and processes.",
  "All samples must be submitted at TI. Missing or inadequate samples mean the vehicle cannot compete in dynamic or endurance events.",
  "Samples must use the same tube material, diameter and thickness as the welds that person makes on Primary roll cage elements.",
  "Every sample must be permanently marked with the school name or initials, the welder name or initials, and the construction date.",
  "Sample 1: a 90° joint, destructively tested. A passing sample fails in the base material, not in the weld metal. Tensile or bending failure is allowed, but the peak stress must be at the weld. Test before the competition and bring both pieces if the sample separates completely.",
  "Sample 2: two tubes joined at 30°, at least 149.86 mm (5.9 in) from the joint centre to the end of each extended leg, and at least 50.8 mm (2 in) on the closed end. Section it along the tube length to show adequate, uniform penetration. Test before the competition and bring both pieces if it separates."
 ],
 "engineering": [
  "This is a process qualification, not a design rule. Build samples from the same heat/lot and the same tube OD/wall as the cage. If you change filler, process, or tube, re-qualify.",
  "Sample 1 is a destructive test to failure; the failure must be in the base metal. If it fails in the weld, the weld procedure or operator is not qualified.",
  "Sample 2 is a 30° angled joint sectioned longitudinally. The 149.86 mm and 50.8 mm dimensions are measured from the joint centre. Keep the marked samples and test records as TI evidence.",
  "Plan the sample schedule early: each welder needs two samples, and the samples must be tested before arrival. Do not leave this to the week before TI."
 ],
 "notes": [
  "Source ambiguity: 'The sample shall comprise a 90° joint, the leg length of which is unrestricted shall be (Figure B-26) be destructively tested.' The sentence is grammatically defective. The intent is that the leg length is unrestricted and the sample is destructively tested; confirm the exact requirement with BTC if challenged.",
  "Formatting artefact: 'www. bajasae.net/go/downloads' printed with a space after 'www.'; normalised to www.bajasae.net/go/downloads."
 ]
},
{
 "id": "B.3.2.16", "title": "Roll Cage Materials", "page": 32, "kind": "requirement", "priority": "High",
 "components": ["Materials & Documentation"],
 "body": [
  "The material used for the Primary Roll Cage Members and bracing shall have a specification minimum yield strength of at least 365 MPa and an as-tested carbon content of at least 0.18%. The wall thickness must be at least 1.6 mm (0.062 in) regardless of material or section size. The bending stiffness and bending strength must be calculated about a neutral axis that gives the minimum values.",
  "• Kb minimum: 2620 Nm²",
  "• Sb minimum: 374 Nm",
  "Note: Docol R8 tubing is permitted without the required carbon content, provided the aforementioned dimensional requirements or equivalencies are met. This material is not intended to undergo any heat treatment after welding and sizing as this may alter the mechanical properties of the material.",
  "Documentation of the materials must include:",
  "1. Invoice(s) of the Primary roll cage materials shall be dated within 5 years of January 1 of the competition year. No exceptions.",
  "2. Material tests or certifications, which specify the carbon content and as-tested yield strength. Manufacturer’s certifications for Primary Material must be dated within 6 years of January 1 of the competition year. No exceptions.",
  "3. For all materials used for Primary material, calculations must be provided proving bending stiffness and bending strength meet or exceed the requirements:",
  "a. Kb minimum: 2620 Nm²",
  "b. Sb minimum: 374 Nm",
  "All calculations shall be typed and submitted through the document portal and brought to TI. All calculations shall be in SI units to three significant figures to the nominal tube sizes as specified by the invoice.",
  "Bending stiffness, kb, is given by: kb = E·I",
  "Where: E - Modulus of elasticity (205 GPa for all steels); I - Second moment of area for the structural cross section.",
  "Bending strength, Sb, is given by: Sb = Sy·I / c",
  "Where: Sy - Yield strength; c - Distance from neutral axis to extreme fibre."
 ],
 "plain": [
  "Primary roll cage material and bracing must have a minimum yield strength of 365 MPa and an as-tested carbon content of at least 0.18%.",
  "Wall thickness must be at least 1.6 mm (0.062 in), regardless of material or section size.",
  "Bending stiffness and strength must be calculated about the neutral axis that gives the minimum values. Kb must be at least 2620 Nm² and Sb at least 374 Nm.",
  "Docol R8 is permitted without the carbon content requirement, provided the dimensional requirements or equivalencies are met. It is not intended for heat treatment after welding and sizing.",
  "Documentation must include: invoices dated within 5 years of 1 January of the competition year (no exceptions); material tests or certifications stating carbon content and as-tested yield strength, with manufacturer certifications dated within 6 years of 1 January of the competition year (no exceptions); and calculations proving Kb and Sb.",
  "Calculations must be typed, submitted through the document portal, brought to TI, in SI units to three significant figures, for the nominal tube sizes on the invoice.",
  "The formulas are kb = E·I and Sb = Sy·I / c, with E = 205 GPa for all steels, I = second moment of area, Sy = yield strength, and c = distance from the neutral axis to the extreme fibre."
 ],
 "engineering": [
  "The 2027 foreword says the carbon requirement is now based on nominal material grade (e.g. 1018), but the rule text still says 'as-tested carbon content of at least 0.18%'. Keep both the invoice (proving the grade purchased) and the material certificate (proving the as-tested carbon and yield). Do not rely on one alone.",
  "Use minimum properties for the calculations: E = 205 GPa, Sy = 365 MPa minimum, and the minimum I/c about the worst neutral axis. For a round tube, I = π(D⁴ − d⁴)/64 and c = D/2; for a rectangle, I = b·h³/12 about the weak axis and c = h/2.",
  "Use the minimum measured wall, not the nominal wall, in the calculation. If the measured wall is below 1.6 mm anywhere, the material fails regardless of the calculated Kb/Sb.",
  "The Kb/Sb check is a section-property check, not a full structural analysis. It confirms the tube is at least as stiff and strong as the baseline; it does not replace a cage load-case analysis.",
  "Docol R8 is an exception on carbon content only — the 1.6 mm wall and Kb/Sb requirements still apply, and no post-weld heat treatment is allowed."
 ],
 "notes": [
  "Potential conflict: the Foreword (p.2) describes a change to nominal carbon content based on material grade, while B.3.2.16 still says 'as-tested carbon content of at least 0.18%'. FEROX approach: retain invoice and certificate for both the nominal grade and the as-tested value; raise a rules inquiry if the certificate shows a different value.",
  "Formatting: the source prints 'Kb' and 'kb' inconsistently and 'Nm2' for Nm². The formulas are reproduced from the printed equations on p.33: kb = E·I and Sb = Sy·I / c."
 ]
},
{
 "id": "B.3.2.17", "title": "Roll Cage Specification Sheet", "page": 33, "kind": "requirement", "priority": "High",
 "components": ["Materials & Documentation", "Roll Cage Documentation"],
 "body": [
  "Each vehicle must present a completed and signed BSC Roll Cage Specification Sheet at TI. Newly completed copies must be presented for each competition."
 ],
 "plain": [
  "Every vehicle must present a completed and signed BSC Roll Cage Specification Sheet at Technical Inspection.",
  "A newly completed copy must be presented for each competition — last season's sheet is not acceptable."
 ],
 "engineering": [
  "This is a controlled document. Fill it from the final CAD and material data, sign it, and bring it to TI. Do not reuse a previous season's sheet.",
  "The sheet is part of the Roll Cage Documentation Package (B.3.7.1) and is reviewed before TI through the document portal (B.3.7.2). Keep the CAD revision and material lot references consistent with the sheet."
 ],
 "notes": ["External dependency: the specification sheet template is not included in the rulebook. Obtain the current BSC template from the organisers and confirm the revision before submission."]
},
{
 "id": "B.3.3", "title": "Driver Clearance", "page": 33, "kind": "parent", "priority": "High",
 "components": ["Driver Clearance"],
 "body": [],
 "plain": ["This is a parent heading. The requirements are in B.3.3.1 (Lateral Space) and B.3.3.2 (Vertical Space)."],
 "engineering": ["Driver clearance is a template/straight-edge test, not a single dimension. Build the clearance model with the driver's full equipment: helmet, suit, gloves, shoes, and restraint harness."],
 "notes": ["B.3.3 has no body text in the source; its subsections carry the requirements."]
},
{
 "id": "B.3.3.1", "title": "Lateral Space", "page": 33, "kind": "requirement", "priority": "High",
 "components": ["Driver Clearance", "Roll Cage — General"],
 "body": [
  "Minimum space is based on clearances between the driver and a straight edge applied to any two points on the outside edge of the roll cage structure. The driver’s helmet shall have 152.4 mm (6 in) clearance, while the driver’s shoulders, torso, hips, thighs, knees, arms, elbows, and hands shall have 76.2 mm (3 in) clearance. Clearances are relative to any and all drivers selected at TI, seated in a normal driving position, and wearing all required equipment.",
  "For any member to contribute to lateral clearance, that member must be listed in B.3.2.2 Primary Members, B.3.2.3 - Secondary Members, or conform to the requirements of B.3.2.8.1 - Gussets for Lateral Clearance or B.3.2.12.1 Gussets for RHO and FBM, otherwise it is assumed to have no contribution (Suspension members, for example, do not contribute to lateral spacing)."
 ],
 "plain": [
  "Lateral clearance is measured between the driver and a straight edge applied to any two points on the outside edge of the roll cage.",
  "The helmet needs 152.4 mm (6 in) clearance. The shoulders, torso, hips, thighs, knees, arms, elbows and hands need 76.2 mm (3 in).",
  "Clearance must hold for any and all drivers selected at TI, seated in a normal driving position and wearing all required equipment.",
  "Only a member listed as Primary (B.3.2.2), Secondary (B.3.2.3), or a qualifying gusset (B.3.2.8.1 or B.3.2.12.1) may count toward lateral clearance. Anything else — suspension members, for example — is assumed to contribute nothing."
 ],
 "engineering": [
  "This is a straight-edge sweep, not a point-to-point dimension. In CAD, build the convex hull between every pair of cage points and check the driver's helmet/body envelope against it.",
  "Only compliant cage members count. Suspension, steering, and bodywork cannot be used to claim lateral clearance; if the cage itself is too narrow, add a qualifying gusset or move the member.",
  "Test the largest driver on the team in full gear, and assume TI may select any driver. A clearance that only works for the smallest driver is not compliant.",
  "Document the driver anthropometry and the equipment used for the check — the clearance is only reproducible if the test condition is recorded."
 ],
 "notes": []
},
{
 "id": "B.3.3.2", "title": "Vertical Space", "page": 34, "kind": "requirement", "priority": "High",
 "components": ["Driver Clearance", "RHO", "RRH", "Lateral Cross Members"],
 "body": [
  "The driver’s helmet shall have 152.4 mm (6 in) minimum clearance from any two points among those members that make up to top of the roll cage. These members are: the RHO members (exclusive of any covering or padding); the RRH upper, LC; and the LC between points C (left and right). In an elevation (side) view, no part of the driver's body, shoes, and clothing may extend beyond the envelope of the roll cage."
 ],
 "plain": [
  "The helmet must have at least 152.4 mm (6 in) clearance from any two points among the members that form the top of the roll cage.",
  "Those members are the RHO (excluding any covering or padding), the RRH upper LC, and the LC between Points C left and right.",
  "In side elevation, no part of the driver's body, shoes or clothing may extend beyond the roll cage envelope."
 ],
 "engineering": [
  "Measure from the helmet's outer surface, with the helmet worn, to the nearest top member using the two-point straight-edge method. Exclude padding and covering from the RHO datum — the structural tube is the reference.",
  "The side-view envelope check means the helmet and head must not project above or ahead of the cage outline. Check with the driver in the normal driving position and with the head turned.",
  "The 152.4 mm is a minimum clearance, not a target. Leave margin for helmet shape, head movement, and seat compression."
 ],
 "notes": []
},
{
 "id": "B.3.4", "title": "Sharp Edges", "page": 34, "kind": "requirement", "priority": "Medium",
 "components": ["Roll Cage — General", "Welding & Fabrication"],
 "body": [
  "The entire vehicle, including the frame, shall have no exposed sharp edges which might endanger the driver, track workers, or people working around the vehicle while the vehicle is in any attitude (static, dynamic, inverted, etc.)."
 ],
 "plain": [
  "The entire vehicle, including the frame, must have no exposed sharp edges that could endanger the driver, track workers, or people around the vehicle in any attitude — static, dynamic, or inverted."
 ],
 "engineering": [
  "Deburr all tube ends, gusset edges, bracket corners, and bolt heads. Consider the inverted attitude: a sharp edge under the frame becomes a hazard in a rollover.",
  "Use a glove test and a visual inspection in all attitudes. Pay particular attention to weld toes, notch roots, and the edges of drilled holes."
 ],
 "notes": ["Scope: this rule applies to the entire vehicle, not only the roll cage."]
},
{
 "id": "B.3.5", "title": "Bolted Roll Cage Joints", "page": 34, "kind": "requirement", "priority": "High",
 "components": ["Bolted Joints", "Roll Cage — General"],
 "body": [
  "Bolted Roll cage joints are acceptable only if the following requirements are met (Figure B-28):",
  "1) Removable members are permitted on non-primary tubes.",
  "2) The tube joint shall be of the design below, constructed to be well-fit and free from injurious defects. Dimensions shown do not include manufacturing tolerances.",
  "3) The only permitted tube sizes for removable members are 25.4 mm (1 in) diameter and 31.75 mm (1.25 in) diameter.",
  "4) The tube joint diameter shall match the diameter of the removable member.",
  "5) The tube joint wall thickness recess shall match the wall thickness of the removable member.",
  "6) Two 6.35 mm (0.25 in) socket head cap screws meeting the requirements of B.12 are required to fasten the tube joint.",
  "7) Nuts used shall meet the requirements of B.12.",
  "8) The tube joint shall be constructed of steel, with a minimum strength requirement matching 1018 steel.",
  "9) Each side of the joint shall have two rosette welds, separated by 180°.",
  "10) Each side of the joint shall be fully welded to the tube of the removable member.",
  "11) Chamfer size C1 shall match the measurement of the wall thickness of the tube.",
  "12) Chamfer size C2 shall nominally be 1.016 mm (0.04 in)"
 ],
 "plain": [
  "Bolted roll cage joints are allowed only if all twelve conditions are met.",
  "Removable members are permitted only on non-primary tubes.",
  "The joint must follow the design in Figure B-28, be well fitted, and free from injurious defects. Dimensions shown do not include manufacturing tolerances.",
  "Only 25.4 mm (1 in) and 31.75 mm (1.25 in) tube sizes may be used for removable members.",
  "The joint diameter must match the removable member, and the wall-thickness recess must match the member's wall.",
  "Two 6.35 mm (0.25 in) socket head cap screws meeting B.12 are required; nuts must also meet B.12.",
  "The joint must be steel with a minimum strength matching 1018 steel.",
  "Each side needs two rosette welds, 180° apart, and must be fully welded to the removable member's tube.",
  "Chamfer C1 equals the tube wall thickness; C2 is nominally 1.016 mm (0.04 in)."
 ],
 "engineering": [
  "Bolted joints are for removable non-primary members (nose tips, access panels, etc.), not for primary structure. Do not use a bolted joint to split a primary member.",
  "The joint is a machined socket with a recessed wall; two cap screws clamp the removable tube. The rosette welds are on the socket side, two per side at 180°.",
  "Figure B-28 contains additional dimensions (0.750, 0.250, 0.040, 0.062, 0.125, 0.1875 in) that are not stated in the text. Use the figure for the full detail; do not reverse-engineer them from the text alone.",
  "Cross-reference B.12 for the cap screws and nuts. Confirm the fastener grade and the nut specification before ordering."
 ],
 "notes": [
  "Figure B-28 dimensions must be read from the source page image; the text only specifies C1 and C2.",
  "Cross-reference: B.12 (Fasteners and Attachments) is outside Article 3 and must be resolved before finalising the joint design."
 ]
},
{
 "id": "B.3.6", "title": "Drilled Members", "page": 35, "kind": "parent", "priority": "Medium",
 "components": ["Drilled Members"],
 "body": [],
 "plain": ["This is a parent heading. The requirements are in B.3.6.1 (Sleeved Joints) and B.3.6.2 (Drilled Holes)."],
 "engineering": ["Treat any hole in a required member as a stress concentrator. Sleeve it under B.3.6.1 unless the single-hole exemption in B.3.6.2 applies."],
 "notes": ["B.3.6 has no body text in the source; its subsections carry the requirements."]
},
{
 "id": "B.3.6.1", "title": "Sleeved Joints", "page": 35, "kind": "requirement", "priority": "High",
 "components": ["Drilled Members", "Roll Cage — General"],
 "body": [
  "Members which need to be drilled through both walls for the purpose of mounting fasteners or routing accessories shall be reinforced with a weld-in sleeve. Sleeves shall be designed to fit tightly on the inside of the hole or joint being reinforced as well as the fastener passing through the sleeve. Sleeves in required members shall be on the tube centreline, have an outer diameter no larger than 0.5 times the member diameter, have a wall thickness greater than or equal to the tube it is welded to and extend beyond the tube on both sides and be fully welded to the tube. An unacceptable joint is denoted by a red “X”. An acceptable joint is denoted by a green “O” in Figure B-28."
 ],
 "plain": [
  "If a member must be drilled through both walls to mount a fastener or route an accessory, it must be reinforced with a weld-in sleeve.",
  "The sleeve must fit tightly inside the hole or joint and around the fastener.",
  "In required members, the sleeve must be on the tube centreline, have an OD no larger than half the member diameter, have a wall at least as thick as the tube, extend beyond the tube on both sides, and be fully welded to the tube.",
  "Figure B-28 (in the source; the figure shown is B-29) marks an unacceptable joint with a red X and an acceptable joint with a green O."
 ],
 "engineering": [
  "This is a common failure: a bolt through a frame tube without a sleeve crushes the tube and creates a fatigue crack. The sleeve carries the bolt load into the tube wall around its full circumference.",
  "Sleeve OD ≤ 0.5 × member OD keeps the material removal acceptable. Wall ≥ tube wall. The sleeve must protrude beyond both walls and be fully welded (fillet around the protruding sleeve).",
  "Keep the sleeve on the tube centreline. An off-centre sleeve creates an eccentric bolt load and a bending stress in the tube."
 ],
 "notes": ["Cross-reference inconsistency: the text says the red X/green O are 'in Figure B-28', but the figure shown on the page is Figure B-29 (Roll Cage, Required sleeve for drilled holes). Treat the figure reference as likely intended B-29."]
},
{
 "id": "B.3.6.2", "title": "Drilled Holes", "page": 35, "kind": "requirement", "priority": "Medium",
 "components": ["Drilled Members"],
 "body": ["Single drilled holes in members with a diameter less than or equal to 5 mm (0.197 in) do not require a sleeve."],
 "plain": ["A single drilled hole with a diameter of 5 mm (0.197 in) or less does not require a sleeve."],
 "engineering": ["The exemption is for a single hole, not a pattern. Measure the hole diameter, not the fastener diameter. If the hole is larger, or there are multiple holes, sleeve it under B.3.6.1."],
 "notes": []
},
{
 "id": "B.3.7", "title": "Roll Cage Documentation Package", "page": 35, "kind": "parent", "priority": "High",
 "components": ["Roll Cage Documentation"],
 "body": [],
 "plain": ["This is a parent heading. The requirements are in B.3.7.1 (Required Documents), B.3.7.2 (Document Submission) and B.3.7.3 (Process)."],
 "engineering": ["Start the package early. The review cycle is typically 30 days after the deadline, and a rejection requires correction and resubmission until the package is Accepted."],
 "notes": ["B.3.7 has no body text in the source; its subsections carry the requirements."]
},
{
 "id": "B.3.7.1", "title": "Required Documents", "page": 35, "kind": "requirement", "priority": "High",
 "components": ["Roll Cage Documentation", "Materials & Documentation"],
 "body": ["Required documents for the Roll Cage Documentation Package include: Roll Cage Specification Sheet & material documentation (invoices, certifications, calculations, etc.) and a single isometric view diagram of the frame highlighting professional fabrication."],
 "plain": ["The documentation package must include the Roll Cage Specification Sheet, the material documentation (invoices, certifications, calculations, etc.), and a single isometric view diagram of the frame highlighting professional fabrication."],
 "engineering": [
  "The isometric diagram is a communication document for the reviewers, not a manufacturing drawing. Use a clean CAD view with the relevant areas highlighted and labelled.",
  "Keep the material documents traceable to the exact tube used (heat/lot). A certificate for a different lot does not support the cage."
 ],
 "notes": ["Ambiguity: 'highlighting professional fabrication' is not defined. B.3.7.2(e) refers to a diagram highlighting parts that were outsourced or professionally fabricated. Confirm whether one diagram must satisfy both descriptions."]
},
{
 "id": "B.3.7.2", "title": "Document Submission", "page": 36, "kind": "requirement", "priority": "High",
 "components": ["Roll Cage Documentation"],
 "body": [
  "1) Upload in a Google Drive Folder the Roll Cage Documentation Package",
  "a. Roll Cage Specification Sheet",
  "b. Invoice of roll cage material",
  "c. Material Test of Certification",
  "d. Any Required Calculation per Rule B.3.2.16 - Roll Cage Materials",
  "e. A diagram highlighting any parts of the frame that were outsourced or professionally fabricated",
  "2) Share the link of the files in Google Drive folder during submission for DR 2 via email to bsc@saeiss.org."
 ],
 "plain": [
  "Upload the package to a Google Drive folder containing: the Roll Cage Specification Sheet, the roll cage material invoice, the material test or certification, any required calculation per B.3.2.16, and a diagram highlighting any frame parts that were outsourced or professionally fabricated.",
  "Share the Drive folder link during the DR 2 submission by email to bsc@saeiss.org."
 ],
 "engineering": [
  "DR 2 is a design review milestone; confirm the exact deadline in Part C / the competition schedule. The Drive folder must be shared with the organisers before the DR 2 submission.",
  "Test the share link in a logged-out browser. A link that requires request access is a submission failure.",
  "The outsourced-parts diagram has cost implications — keep it consistent with the cost report and the frame fabrication costing rules. Do not under-report outsourced work."
 ],
 "notes": [
  "Cross-reference: 'DR 2' is referenced in B.3.7.2 but not defined in Article 3. Resolve the definition and deadline in Part C (Static Events / Design Evaluation).",
  "Wording: 'Material Test of Certification' appears to mean 'Material Test or Certification'; reproduced as printed."
 ]
},
{
 "id": "B.3.7.3", "title": "Process", "page": 36, "kind": "requirement", "priority": "Medium",
 "components": ["Roll Cage Documentation"],
 "body": ["Documents shall be reviewed by the Technical Inspectors on a first come, first serve basis. Typical review period shall be thirty (30) days after the deadline. After review, feedback shall be given to teams. If the submission is rejected by the BSCTI, the team must correct the error noted in the rejection and continue to resubmit the Roll Cage Documentation Package, until they are marked Accepted. It is the responsibility of teams to submit complete documents by the appropriate deadlines. If teams have additional questions, they shall need to use other resources to find the answers or wait until competition."],
 "plain": [
  "Technical Inspectors review documents first come, first served. The typical review period is 30 days after the deadline.",
  "Feedback is given after review. If the submission is rejected, the team must correct the noted error and resubmit until it is marked Accepted.",
  "Teams are responsible for submitting complete documents by the deadlines. Additional questions must be answered from other resources or waited on until the competition."
 ],
 "engineering": [
  "Build a 30-day buffer before the deadline. A rejection can cost a full review cycle and delay the DR 2 gate.",
  "Track the package status as a project gate: Draft → Submitted → Under Review → Rejected / Accepted. A rejected package is not a document problem only; it can block the whole design review.",
  "Keep a change log of what was corrected between submissions so the resubmission is auditable."
 ],
 "notes": []
}
]
