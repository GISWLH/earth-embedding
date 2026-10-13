# Vendored subset of microsoft/satclip@1ead1067e9a00d44b132403b6bb2ce061e48d48e
# satclip/positional_encoding/spherical_harmonics_ylm.py, truncated to degrees l <= 39
# (functions Yl0_m0 .. Yl39_m39, sufficient for legendre_polys <= 40). Upstream full-file
# SHA-256: facf06de2c98b6cc9ec7f6cbc2f73b8c94ff6dd43076e6607bf99b6e75078097. MIT License.
# ruff: noqa
"""
analytic expressions of spherical harmonics generated with sympy file 
Marc Russwurm generated 2023-07-26

run 
python spherical_harmonics_generate_ylms.py > spherical_harmonics_ylm.py

to generate the source code
"""

import torch
from torch import cos, sin

def get_SH(m,l):
  fname = f"Yl{l}_m{m}".replace("-","_minus_")
  return globals()[fname]

def SH(m, l, phi, theta):
  Ylm = get_SH(m,l)
  return Ylm(theta, phi)



#@torch.jit.script
def Yl0_m0(theta, phi):
    return 0.886226925452758

#@torch.jit.script
def Yl1_m_minus_1(theta, phi):
    return 0.48860251190292*(1.0 - cos(theta)**2)**0.5*sin(phi)

#@torch.jit.script
def Yl1_m0(theta, phi):
    return 1.53499006191973*cos(theta)

#@torch.jit.script
def Yl1_m1(theta, phi):
    return 0.48860251190292*(1.0 - cos(theta)**2)**0.5*cos(phi)

#@torch.jit.script
def Yl2_m_minus_2(theta, phi):
    return 0.18209140509868*(3.0 - 3.0*cos(theta)**2)*sin(2*phi)

#@torch.jit.script
def Yl2_m_minus_1(theta, phi):
    return 1.09254843059208*(1.0 - cos(theta)**2)**0.5*sin(phi)*cos(theta)

#@torch.jit.script
def Yl2_m0(theta, phi):
    return 2.97249547320451*cos(theta)**2 - 0.990831824401503

#@torch.jit.script
def Yl2_m1(theta, phi):
    return 1.09254843059208*(1.0 - cos(theta)**2)**0.5*cos(phi)*cos(theta)

#@torch.jit.script
def Yl2_m2(theta, phi):
    return 0.18209140509868*(3.0 - 3.0*cos(theta)**2)*cos(2*phi)

#@torch.jit.script
def Yl3_m_minus_3(theta, phi):
    return 0.590043589926644*(1.0 - cos(theta)**2)**1.5*sin(3*phi)

#@torch.jit.script
def Yl3_m_minus_2(theta, phi):
    return 1.44530572132028*(1.0 - cos(theta)**2)*sin(2*phi)*cos(theta)

#@torch.jit.script
def Yl3_m_minus_1(theta, phi):
    return 0.304697199642977*(1.0 - cos(theta)**2)**0.5*(7.5*cos(theta)**2 - 1.5)*sin(phi)

#@torch.jit.script
def Yl3_m0(theta, phi):
    return 5.86184012479344*cos(theta)**3 - 3.51710407487606*cos(theta)

#@torch.jit.script
def Yl3_m1(theta, phi):
    return 0.304697199642977*(1.0 - cos(theta)**2)**0.5*(7.5*cos(theta)**2 - 1.5)*cos(phi)

#@torch.jit.script
def Yl3_m2(theta, phi):
    return 1.44530572132028*(1.0 - cos(theta)**2)*cos(2*phi)*cos(theta)

#@torch.jit.script
def Yl3_m3(theta, phi):
    return 0.590043589926644*(1.0 - cos(theta)**2)**1.5*cos(3*phi)

#@torch.jit.script
def Yl4_m_minus_4(theta, phi):
    return 0.625835735449176*(1.0 - cos(theta)**2)**2*sin(4*phi)

#@torch.jit.script
def Yl4_m_minus_3(theta, phi):
    return 1.77013076977993*(1.0 - cos(theta)**2)**1.5*sin(3*phi)*cos(theta)

#@torch.jit.script
def Yl4_m_minus_2(theta, phi):
    return 0.063078313050504*(1.0 - cos(theta)**2)*(52.5*cos(theta)**2 - 7.5)*sin(2*phi)

#@torch.jit.script
def Yl4_m_minus_1(theta, phi):
    return 0.267618617422916*(1.0 - cos(theta)**2)**0.5*(17.5*cos(theta)**3 - 7.5*cos(theta))*sin(phi)

#@torch.jit.script
def Yl4_m0(theta, phi):
    return 11.6317283965674*cos(theta)**4 - 9.97005291134353*cos(theta)**2 + 0.997005291134353

#@torch.jit.script
def Yl4_m1(theta, phi):
    return 0.267618617422916*(1.0 - cos(theta)**2)**0.5*(17.5*cos(theta)**3 - 7.5*cos(theta))*cos(phi)

#@torch.jit.script
def Yl4_m2(theta, phi):
    return 0.063078313050504*(1.0 - cos(theta)**2)*(52.5*cos(theta)**2 - 7.5)*cos(2*phi)

#@torch.jit.script
def Yl4_m3(theta, phi):
    return 1.77013076977993*(1.0 - cos(theta)**2)**1.5*cos(3*phi)*cos(theta)

#@torch.jit.script
def Yl4_m4(theta, phi):
    return 0.625835735449176*(1.0 - cos(theta)**2)**2*cos(4*phi)

#@torch.jit.script
def Yl5_m_minus_5(theta, phi):
    return 0.65638205684017*(1.0 - cos(theta)**2)**2.5*sin(5*phi)

#@torch.jit.script
def Yl5_m_minus_4(theta, phi):
    return 2.07566231488104*(1.0 - cos(theta)**2)**2*sin(4*phi)*cos(theta)

#@torch.jit.script
def Yl5_m_minus_3(theta, phi):
    return 0.00931882475114763*(1.0 - cos(theta)**2)**1.5*(472.5*cos(theta)**2 - 52.5)*sin(3*phi)

#@torch.jit.script
def Yl5_m_minus_2(theta, phi):
    return 0.0456527312854602*(1.0 - cos(theta)**2)*(157.5*cos(theta)**3 - 52.5*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl5_m_minus_1(theta, phi):
    return 0.241571547304372*(1.0 - cos(theta)**2)**0.5*(39.375*cos(theta)**4 - 26.25*cos(theta)**2 + 1.875)*sin(phi)

#@torch.jit.script
def Yl5_m0(theta, phi):
    return 23.1468472528419*cos(theta)**5 - 25.7187191698243*cos(theta)**3 + 5.51115410781949*cos(theta)

#@torch.jit.script
def Yl5_m1(theta, phi):
    return 0.241571547304372*(1.0 - cos(theta)**2)**0.5*(39.375*cos(theta)**4 - 26.25*cos(theta)**2 + 1.875)*cos(phi)

#@torch.jit.script
def Yl5_m2(theta, phi):
    return 0.0456527312854602*(1.0 - cos(theta)**2)*(157.5*cos(theta)**3 - 52.5*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl5_m3(theta, phi):
    return 0.00931882475114763*(1.0 - cos(theta)**2)**1.5*(472.5*cos(theta)**2 - 52.5)*cos(3*phi)

#@torch.jit.script
def Yl5_m4(theta, phi):
    return 2.07566231488104*(1.0 - cos(theta)**2)**2*cos(4*phi)*cos(theta)

#@torch.jit.script
def Yl5_m5(theta, phi):
    return 0.65638205684017*(1.0 - cos(theta)**2)**2.5*cos(5*phi)

#@torch.jit.script
def Yl6_m_minus_6(theta, phi):
    return 0.683184105191914*(1.0 - cos(theta)**2)**3*sin(6*phi)

#@torch.jit.script
def Yl6_m_minus_5(theta, phi):
    return 2.36661916223175*(1.0 - cos(theta)**2)**2.5*sin(5*phi)*cos(theta)

#@torch.jit.script
def Yl6_m_minus_4(theta, phi):
    return 0.0010678622237645*(1.0 - cos(theta)**2)**2*(5197.5*cos(theta)**2 - 472.5)*sin(4*phi)

#@torch.jit.script
def Yl6_m_minus_3(theta, phi):
    return 0.00584892228263444*(1.0 - cos(theta)**2)**1.5*(1732.5*cos(theta)**3 - 472.5*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl6_m_minus_2(theta, phi):
    return 0.0350935336958066*(1.0 - cos(theta)**2)*(433.125*cos(theta)**4 - 236.25*cos(theta)**2 + 13.125)*sin(2*phi)

#@torch.jit.script
def Yl6_m_minus_1(theta, phi):
    return 0.221950995245231*(1.0 - cos(theta)**2)**0.5*(86.625*cos(theta)**5 - 78.75*cos(theta)**3 + 13.125*cos(theta))*sin(phi)

#@torch.jit.script
def Yl6_m0(theta, phi):
    return 46.1326724717039*cos(theta)**6 - 62.9081897341417*cos(theta)**4 + 20.9693965780472*cos(theta)**2 - 0.998542694192725

#@torch.jit.script
def Yl6_m1(theta, phi):
    return 0.221950995245231*(1.0 - cos(theta)**2)**0.5*(86.625*cos(theta)**5 - 78.75*cos(theta)**3 + 13.125*cos(theta))*cos(phi)

#@torch.jit.script
def Yl6_m2(theta, phi):
    return 0.0350935336958066*(1.0 - cos(theta)**2)*(433.125*cos(theta)**4 - 236.25*cos(theta)**2 + 13.125)*cos(2*phi)

#@torch.jit.script
def Yl6_m3(theta, phi):
    return 0.00584892228263444*(1.0 - cos(theta)**2)**1.5*(1732.5*cos(theta)**3 - 472.5*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl6_m4(theta, phi):
    return 0.0010678622237645*(1.0 - cos(theta)**2)**2*(5197.5*cos(theta)**2 - 472.5)*cos(4*phi)

#@torch.jit.script
def Yl6_m5(theta, phi):
    return 2.36661916223175*(1.0 - cos(theta)**2)**2.5*cos(5*phi)*cos(theta)

#@torch.jit.script
def Yl6_m6(theta, phi):
    return 0.683184105191914*(1.0 - cos(theta)**2)**3*cos(6*phi)

#@torch.jit.script
def Yl7_m_minus_7(theta, phi):
    return 0.707162732524596*(1.0 - cos(theta)**2)**3.5*sin(7*phi)

#@torch.jit.script
def Yl7_m_minus_6(theta, phi):
    return 2.6459606618019*(1.0 - cos(theta)**2)**3*sin(6*phi)*cos(theta)

#@torch.jit.script
def Yl7_m_minus_5(theta, phi):
    return 9.98394571852353e-5*(1.0 - cos(theta)**2)**2.5*(67567.5*cos(theta)**2 - 5197.5)*sin(5*phi)

#@torch.jit.script
def Yl7_m_minus_4(theta, phi):
    return 0.000599036743111412*(1.0 - cos(theta)**2)**2*(22522.5*cos(theta)**3 - 5197.5*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl7_m_minus_3(theta, phi):
    return 0.00397356022507413*(1.0 - cos(theta)**2)**1.5*(5630.625*cos(theta)**4 - 2598.75*cos(theta)**2 + 118.125)*sin(3*phi)

#@torch.jit.script
def Yl7_m_minus_2(theta, phi):
    return 0.0280973138060306*(1.0 - cos(theta)**2)*(1126.125*cos(theta)**5 - 866.25*cos(theta)**3 + 118.125*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl7_m_minus_1(theta, phi):
    return 0.206472245902897*(1.0 - cos(theta)**2)**0.5*(187.6875*cos(theta)**6 - 216.5625*cos(theta)**4 + 59.0625*cos(theta)**2 - 2.1875)*sin(phi)

#@torch.jit.script
def Yl7_m0(theta, phi):
    return 92.0296731793493*cos(theta)**7 - 148.663318212795*cos(theta)**5 + 67.5742355512704*cos(theta)**3 - 7.5082483945856*cos(theta)

#@torch.jit.script
def Yl7_m1(theta, phi):
    return 0.206472245902897*(1.0 - cos(theta)**2)**0.5*(187.6875*cos(theta)**6 - 216.5625*cos(theta)**4 + 59.0625*cos(theta)**2 - 2.1875)*cos(phi)

#@torch.jit.script
def Yl7_m2(theta, phi):
    return 0.0280973138060306*(1.0 - cos(theta)**2)*(1126.125*cos(theta)**5 - 866.25*cos(theta)**3 + 118.125*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl7_m3(theta, phi):
    return 0.00397356022507413*(1.0 - cos(theta)**2)**1.5*(5630.625*cos(theta)**4 - 2598.75*cos(theta)**2 + 118.125)*cos(3*phi)

#@torch.jit.script
def Yl7_m4(theta, phi):
    return 0.000599036743111412*(1.0 - cos(theta)**2)**2*(22522.5*cos(theta)**3 - 5197.5*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl7_m5(theta, phi):
    return 9.98394571852353e-5*(1.0 - cos(theta)**2)**2.5*(67567.5*cos(theta)**2 - 5197.5)*cos(5*phi)

#@torch.jit.script
def Yl7_m6(theta, phi):
    return 2.6459606618019*(1.0 - cos(theta)**2)**3*cos(6*phi)*cos(theta)

#@torch.jit.script
def Yl7_m7(theta, phi):
    return 0.707162732524596*(1.0 - cos(theta)**2)**3.5*cos(7*phi)

#@torch.jit.script
def Yl8_m_minus_8(theta, phi):
    return 0.72892666017483*(1.0 - cos(theta)**2)**4*sin(8*phi)

#@torch.jit.script
def Yl8_m_minus_7(theta, phi):
    return 2.91570664069932*(1.0 - cos(theta)**2)**3.5*sin(7*phi)*cos(theta)

#@torch.jit.script
def Yl8_m_minus_6(theta, phi):
    return 7.87853281621404e-6*(1.0 - cos(theta)**2)**3*(1013512.5*cos(theta)**2 - 67567.5)*sin(6*phi)

#@torch.jit.script
def Yl8_m_minus_5(theta, phi):
    return 5.10587282657803e-5*(1.0 - cos(theta)**2)**2.5*(337837.5*cos(theta)**3 - 67567.5*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl8_m_minus_4(theta, phi):
    return 0.000368189725644507*(1.0 - cos(theta)**2)**2*(84459.375*cos(theta)**4 - 33783.75*cos(theta)**2 + 1299.375)*sin(4*phi)

#@torch.jit.script
def Yl8_m_minus_3(theta, phi):
    return 0.0028519853513317*(1.0 - cos(theta)**2)**1.5*(16891.875*cos(theta)**5 - 11261.25*cos(theta)**3 + 1299.375*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl8_m_minus_2(theta, phi):
    return 0.0231696385236779*(1.0 - cos(theta)**2)*(2815.3125*cos(theta)**6 - 2815.3125*cos(theta)**4 + 649.6875*cos(theta)**2 - 19.6875)*sin(2*phi)

#@torch.jit.script
def Yl8_m_minus_1(theta, phi):
    return 0.193851103820053*(1.0 - cos(theta)**2)**0.5*(402.1875*cos(theta)**7 - 563.0625*cos(theta)**5 + 216.5625*cos(theta)**3 - 19.6875*cos(theta))*sin(phi)

#@torch.jit.script
def Yl8_m0(theta, phi):
    return 183.699503695146*cos(theta)**8 - 342.905740230939*cos(theta)**6 + 197.830234748619*cos(theta)**4 - 35.9691335906579*cos(theta)**2 + 0.999142599740499

#@torch.jit.script
def Yl8_m1(theta, phi):
    return 0.193851103820053*(1.0 - cos(theta)**2)**0.5*(402.1875*cos(theta)**7 - 563.0625*cos(theta)**5 + 216.5625*cos(theta)**3 - 19.6875*cos(theta))*cos(phi)

#@torch.jit.script
def Yl8_m2(theta, phi):
    return 0.0231696385236779*(1.0 - cos(theta)**2)*(2815.3125*cos(theta)**6 - 2815.3125*cos(theta)**4 + 649.6875*cos(theta)**2 - 19.6875)*cos(2*phi)

#@torch.jit.script
def Yl8_m3(theta, phi):
    return 0.0028519853513317*(1.0 - cos(theta)**2)**1.5*(16891.875*cos(theta)**5 - 11261.25*cos(theta)**3 + 1299.375*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl8_m4(theta, phi):
    return 0.000368189725644507*(1.0 - cos(theta)**2)**2*(84459.375*cos(theta)**4 - 33783.75*cos(theta)**2 + 1299.375)*cos(4*phi)

#@torch.jit.script
def Yl8_m5(theta, phi):
    return 5.10587282657803e-5*(1.0 - cos(theta)**2)**2.5*(337837.5*cos(theta)**3 - 67567.5*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl8_m6(theta, phi):
    return 7.87853281621404e-6*(1.0 - cos(theta)**2)**3*(1013512.5*cos(theta)**2 - 67567.5)*cos(6*phi)

#@torch.jit.script
def Yl8_m7(theta, phi):
    return 2.91570664069932*(1.0 - cos(theta)**2)**3.5*cos(7*phi)*cos(theta)

#@torch.jit.script
def Yl8_m8(theta, phi):
    return 0.72892666017483*(1.0 - cos(theta)**2)**4*cos(8*phi)

#@torch.jit.script
def Yl9_m_minus_9(theta, phi):
    return 0.748900951853188*(1.0 - cos(theta)**2)**4.5*sin(9*phi)

#@torch.jit.script
def Yl9_m_minus_8(theta, phi):
    return 3.1773176489547*(1.0 - cos(theta)**2)**4*sin(8*phi)*cos(theta)

#@torch.jit.script
def Yl9_m_minus_7(theta, phi):
    return 5.37640612566745e-7*(1.0 - cos(theta)**2)**3.5*(17229712.5*cos(theta)**2 - 1013512.5)*sin(7*phi)

#@torch.jit.script
def Yl9_m_minus_6(theta, phi):
    return 3.72488342871223e-6*(1.0 - cos(theta)**2)**3*(5743237.5*cos(theta)**3 - 1013512.5*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl9_m_minus_5(theta, phi):
    return 2.88528229719329e-5*(1.0 - cos(theta)**2)**2.5*(1435809.375*cos(theta)**4 - 506756.25*cos(theta)**2 + 16891.875)*sin(5*phi)

#@torch.jit.script
def Yl9_m_minus_4(theta, phi):
    return 0.000241400036332803*(1.0 - cos(theta)**2)**2*(287161.875*cos(theta)**5 - 168918.75*cos(theta)**3 + 16891.875*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl9_m_minus_3(theta, phi):
    return 0.00213198739401417*(1.0 - cos(theta)**2)**1.5*(47860.3125*cos(theta)**6 - 42229.6875*cos(theta)**4 + 8445.9375*cos(theta)**2 - 216.5625)*sin(3*phi)

#@torch.jit.script
def Yl9_m_minus_2(theta, phi):
    return 0.0195399872275232*(1.0 - cos(theta)**2)*(6837.1875*cos(theta)**7 - 8445.9375*cos(theta)**5 + 2815.3125*cos(theta)**3 - 216.5625*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl9_m_minus_1(theta, phi):
    return 0.183301328077446*(1.0 - cos(theta)**2)**0.5*(854.6484375*cos(theta)**8 - 1407.65625*cos(theta)**6 + 703.828125*cos(theta)**4 - 108.28125*cos(theta)**2 + 2.4609375)*sin(phi)

#@torch.jit.script
def Yl9_m0(theta, phi):
    return 366.831595457261*cos(theta)**9 - 776.819849203611*cos(theta)**7 + 543.773894442528*cos(theta)**5 - 139.429203703212*cos(theta)**3 + 9.50653661612811*cos(theta)

#@torch.jit.script
def Yl9_m1(theta, phi):
    return 0.183301328077446*(1.0 - cos(theta)**2)**0.5*(854.6484375*cos(theta)**8 - 1407.65625*cos(theta)**6 + 703.828125*cos(theta)**4 - 108.28125*cos(theta)**2 + 2.4609375)*cos(phi)

#@torch.jit.script
def Yl9_m2(theta, phi):
    return 0.0195399872275232*(1.0 - cos(theta)**2)*(6837.1875*cos(theta)**7 - 8445.9375*cos(theta)**5 + 2815.3125*cos(theta)**3 - 216.5625*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl9_m3(theta, phi):
    return 0.00213198739401417*(1.0 - cos(theta)**2)**1.5*(47860.3125*cos(theta)**6 - 42229.6875*cos(theta)**4 + 8445.9375*cos(theta)**2 - 216.5625)*cos(3*phi)

#@torch.jit.script
def Yl9_m4(theta, phi):
    return 0.000241400036332803*(1.0 - cos(theta)**2)**2*(287161.875*cos(theta)**5 - 168918.75*cos(theta)**3 + 16891.875*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl9_m5(theta, phi):
    return 2.88528229719329e-5*(1.0 - cos(theta)**2)**2.5*(1435809.375*cos(theta)**4 - 506756.25*cos(theta)**2 + 16891.875)*cos(5*phi)

#@torch.jit.script
def Yl9_m6(theta, phi):
    return 3.72488342871223e-6*(1.0 - cos(theta)**2)**3*(5743237.5*cos(theta)**3 - 1013512.5*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl9_m7(theta, phi):
    return 5.37640612566745e-7*(1.0 - cos(theta)**2)**3.5*(17229712.5*cos(theta)**2 - 1013512.5)*cos(7*phi)

#@torch.jit.script
def Yl9_m8(theta, phi):
    return 3.1773176489547*(1.0 - cos(theta)**2)**4*cos(8*phi)*cos(theta)

#@torch.jit.script
def Yl9_m9(theta, phi):
    return 0.748900951853188*(1.0 - cos(theta)**2)**4.5*cos(9*phi)

#@torch.jit.script
def Yl10_m_minus_10(theta, phi):
    return 0.76739511822199*(1.0 - cos(theta)**2)**5*sin(10*phi)

#@torch.jit.script
def Yl10_m_minus_9(theta, phi):
    return 3.43189529989171*(1.0 - cos(theta)**2)**4.5*sin(9*phi)*cos(theta)

#@torch.jit.script
def Yl10_m_minus_8(theta, phi):
    return 3.23120268385452e-8*(1.0 - cos(theta)**2)**4*(327364537.5*cos(theta)**2 - 17229712.5)*sin(8*phi)

#@torch.jit.script
def Yl10_m_minus_7(theta, phi):
    return 2.37443934928654e-7*(1.0 - cos(theta)**2)**3.5*(109121512.5*cos(theta)**3 - 17229712.5*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl10_m_minus_6(theta, phi):
    return 1.95801284774625e-6*(1.0 - cos(theta)**2)**3*(27280378.125*cos(theta)**4 - 8614856.25*cos(theta)**2 + 253378.125)*sin(6*phi)

#@torch.jit.script
def Yl10_m_minus_5(theta, phi):
    return 1.75129993135143e-5*(1.0 - cos(theta)**2)**2.5*(5456075.625*cos(theta)**5 - 2871618.75*cos(theta)**3 + 253378.125*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl10_m_minus_4(theta, phi):
    return 0.000166142899475011*(1.0 - cos(theta)**2)**2*(909345.9375*cos(theta)**6 - 717904.6875*cos(theta)**4 + 126689.0625*cos(theta)**2 - 2815.3125)*sin(4*phi)

#@torch.jit.script
def Yl10_m_minus_3(theta, phi):
    return 0.00164473079210685*(1.0 - cos(theta)**2)**1.5*(129906.5625*cos(theta)**7 - 143580.9375*cos(theta)**5 + 42229.6875*cos(theta)**3 - 2815.3125*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl10_m_minus_2(theta, phi):
    return 0.0167730288071195*(1.0 - cos(theta)**2)*(16238.3203125*cos(theta)**8 - 23930.15625*cos(theta)**6 + 10557.421875*cos(theta)**4 - 1407.65625*cos(theta)**2 + 27.0703125)*sin(2*phi)

#@torch.jit.script
def Yl10_m_minus_1(theta, phi):
    return 0.174310428544485*(1.0 - cos(theta)**2)**0.5*(1804.2578125*cos(theta)**9 - 3418.59375*cos(theta)**7 + 2111.484375*cos(theta)**5 - 469.21875*cos(theta)**3 + 27.0703125*cos(theta))*sin(phi)

#@torch.jit.script
def Yl10_m0(theta, phi):
    return 732.745538033921*cos(theta)**10 - 1735.44995850139*cos(theta)**8 + 1429.19408347173*cos(theta)**6 - 476.398027823912*cos(theta)**4 + 54.9690032104513*cos(theta)**2 - 0.999436422008206

#@torch.jit.script
def Yl10_m1(theta, phi):
    return 0.174310428544485*(1.0 - cos(theta)**2)**0.5*(1804.2578125*cos(theta)**9 - 3418.59375*cos(theta)**7 + 2111.484375*cos(theta)**5 - 469.21875*cos(theta)**3 + 27.0703125*cos(theta))*cos(phi)

#@torch.jit.script
def Yl10_m2(theta, phi):
    return 0.0167730288071195*(1.0 - cos(theta)**2)*(16238.3203125*cos(theta)**8 - 23930.15625*cos(theta)**6 + 10557.421875*cos(theta)**4 - 1407.65625*cos(theta)**2 + 27.0703125)*cos(2*phi)

#@torch.jit.script
def Yl10_m3(theta, phi):
    return 0.00164473079210685*(1.0 - cos(theta)**2)**1.5*(129906.5625*cos(theta)**7 - 143580.9375*cos(theta)**5 + 42229.6875*cos(theta)**3 - 2815.3125*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl10_m4(theta, phi):
    return 0.000166142899475011*(1.0 - cos(theta)**2)**2*(909345.9375*cos(theta)**6 - 717904.6875*cos(theta)**4 + 126689.0625*cos(theta)**2 - 2815.3125)*cos(4*phi)

#@torch.jit.script
def Yl10_m5(theta, phi):
    return 1.75129993135143e-5*(1.0 - cos(theta)**2)**2.5*(5456075.625*cos(theta)**5 - 2871618.75*cos(theta)**3 + 253378.125*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl10_m6(theta, phi):
    return 1.95801284774625e-6*(1.0 - cos(theta)**2)**3*(27280378.125*cos(theta)**4 - 8614856.25*cos(theta)**2 + 253378.125)*cos(6*phi)

#@torch.jit.script
def Yl10_m7(theta, phi):
    return 2.37443934928654e-7*(1.0 - cos(theta)**2)**3.5*(109121512.5*cos(theta)**3 - 17229712.5*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl10_m8(theta, phi):
    return 3.23120268385452e-8*(1.0 - cos(theta)**2)**4*(327364537.5*cos(theta)**2 - 17229712.5)*cos(8*phi)

#@torch.jit.script
def Yl10_m9(theta, phi):
    return 3.43189529989171*(1.0 - cos(theta)**2)**4.5*cos(9*phi)*cos(theta)

#@torch.jit.script
def Yl10_m10(theta, phi):
    return 0.76739511822199*(1.0 - cos(theta)**2)**5*cos(10*phi)

#@torch.jit.script
def Yl11_m_minus_11(theta, phi):
    return 0.784642105787197*(1.0 - cos(theta)**2)**5.5*sin(11*phi)

#@torch.jit.script
def Yl11_m_minus_10(theta, phi):
    return 3.68029769880531*(1.0 - cos(theta)**2)**5*sin(10*phi)*cos(theta)

#@torch.jit.script
def Yl11_m_minus_9(theta, phi):
    return 1.73470916587426e-9*(1.0 - cos(theta)**2)**4.5*(6874655287.5*cos(theta)**2 - 327364537.5)*sin(9*phi)

#@torch.jit.script
def Yl11_m_minus_8(theta, phi):
    return 1.34369994198887e-8*(1.0 - cos(theta)**2)**4*(2291551762.5*cos(theta)**3 - 327364537.5*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl11_m_minus_7(theta, phi):
    return 1.17141045151419e-7*(1.0 - cos(theta)**2)**3.5*(572887940.625*cos(theta)**4 - 163682268.75*cos(theta)**2 + 4307428.125)*sin(7*phi)

#@torch.jit.script
def Yl11_m_minus_6(theta, phi):
    return 1.11129753051333e-6*(1.0 - cos(theta)**2)**3*(114577588.125*cos(theta)**5 - 54560756.25*cos(theta)**3 + 4307428.125*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl11_m_minus_5(theta, phi):
    return 1.12235548974089e-5*(1.0 - cos(theta)**2)**2.5*(19096264.6875*cos(theta)**6 - 13640189.0625*cos(theta)**4 + 2153714.0625*cos(theta)**2 - 42229.6875)*sin(5*phi)

#@torch.jit.script
def Yl11_m_minus_4(theta, phi):
    return 0.0001187789403385*(1.0 - cos(theta)**2)**2*(2728037.8125*cos(theta)**7 - 2728037.8125*cos(theta)**5 + 717904.6875*cos(theta)**3 - 42229.6875*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl11_m_minus_3(theta, phi):
    return 0.00130115809959914*(1.0 - cos(theta)**2)**1.5*(341004.7265625*cos(theta)**8 - 454672.96875*cos(theta)**6 + 179476.171875*cos(theta)**4 - 21114.84375*cos(theta)**2 + 351.9140625)*sin(3*phi)

#@torch.jit.script
def Yl11_m_minus_2(theta, phi):
    return 0.0146054634441776*(1.0 - cos(theta)**2)*(37889.4140625*cos(theta)**9 - 64953.28125*cos(theta)**7 + 35895.234375*cos(theta)**5 - 7038.28125*cos(theta)**3 + 351.9140625*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl11_m_minus_1(theta, phi):
    return 0.166527904912351*(1.0 - cos(theta)**2)**0.5*(3788.94140625*cos(theta)**10 - 8119.16015625*cos(theta)**8 + 5982.5390625*cos(theta)**6 - 1759.5703125*cos(theta)**4 + 175.95703125*cos(theta)**2 - 2.70703125)*sin(phi)

#@torch.jit.script
def Yl11_m0(theta, phi):
    return 1463.97635620462*cos(theta)**11 - 3834.22379005971*cos(theta)**9 + 3632.4225379513*cos(theta)**7 - 1495.70339797995*cos(theta)**5 + 249.283899663325*cos(theta)**3 - 11.5054107536919*cos(theta)

#@torch.jit.script
def Yl11_m1(theta, phi):
    return 0.166527904912351*(1.0 - cos(theta)**2)**0.5*(3788.94140625*cos(theta)**10 - 8119.16015625*cos(theta)**8 + 5982.5390625*cos(theta)**6 - 1759.5703125*cos(theta)**4 + 175.95703125*cos(theta)**2 - 2.70703125)*cos(phi)

#@torch.jit.script
def Yl11_m2(theta, phi):
    return 0.0146054634441776*(1.0 - cos(theta)**2)*(37889.4140625*cos(theta)**9 - 64953.28125*cos(theta)**7 + 35895.234375*cos(theta)**5 - 7038.28125*cos(theta)**3 + 351.9140625*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl11_m3(theta, phi):
    return 0.00130115809959914*(1.0 - cos(theta)**2)**1.5*(341004.7265625*cos(theta)**8 - 454672.96875*cos(theta)**6 + 179476.171875*cos(theta)**4 - 21114.84375*cos(theta)**2 + 351.9140625)*cos(3*phi)

#@torch.jit.script
def Yl11_m4(theta, phi):
    return 0.0001187789403385*(1.0 - cos(theta)**2)**2*(2728037.8125*cos(theta)**7 - 2728037.8125*cos(theta)**5 + 717904.6875*cos(theta)**3 - 42229.6875*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl11_m5(theta, phi):
    return 1.12235548974089e-5*(1.0 - cos(theta)**2)**2.5*(19096264.6875*cos(theta)**6 - 13640189.0625*cos(theta)**4 + 2153714.0625*cos(theta)**2 - 42229.6875)*cos(5*phi)

#@torch.jit.script
def Yl11_m6(theta, phi):
    return 1.11129753051333e-6*(1.0 - cos(theta)**2)**3*(114577588.125*cos(theta)**5 - 54560756.25*cos(theta)**3 + 4307428.125*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl11_m7(theta, phi):
    return 1.17141045151419e-7*(1.0 - cos(theta)**2)**3.5*(572887940.625*cos(theta)**4 - 163682268.75*cos(theta)**2 + 4307428.125)*cos(7*phi)

#@torch.jit.script
def Yl11_m8(theta, phi):
    return 1.34369994198887e-8*(1.0 - cos(theta)**2)**4*(2291551762.5*cos(theta)**3 - 327364537.5*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl11_m9(theta, phi):
    return 1.73470916587426e-9*(1.0 - cos(theta)**2)**4.5*(6874655287.5*cos(theta)**2 - 327364537.5)*cos(9*phi)

#@torch.jit.script
def Yl11_m10(theta, phi):
    return 3.68029769880531*(1.0 - cos(theta)**2)**5*cos(10*phi)*cos(theta)

#@torch.jit.script
def Yl11_m11(theta, phi):
    return 0.784642105787197*(1.0 - cos(theta)**2)**5.5*cos(11*phi)

#@torch.jit.script
def Yl12_m_minus_12(theta, phi):
    return 0.800821995783972*(1.0 - cos(theta)**2)**6*sin(12*phi)

#@torch.jit.script
def Yl12_m_minus_11(theta, phi):
    return 3.92321052893598*(1.0 - cos(theta)**2)**5.5*sin(11*phi)*cos(theta)

#@torch.jit.script
def Yl12_m_minus_10(theta, phi):
    return 8.4141794839602e-11*(1.0 - cos(theta)**2)**5*(158117071612.5*cos(theta)**2 - 6874655287.5)*sin(10*phi)

#@torch.jit.script
def Yl12_m_minus_9(theta, phi):
    return 6.83571172711927e-10*(1.0 - cos(theta)**2)**4.5*(52705690537.5*cos(theta)**3 - 6874655287.5*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl12_m_minus_8(theta, phi):
    return 6.26503328368427e-9*(1.0 - cos(theta)**2)**4*(13176422634.375*cos(theta)**4 - 3437327643.75*cos(theta)**2 + 81841134.375)*sin(8*phi)

#@torch.jit.script
def Yl12_m_minus_7(theta, phi):
    return 6.26503328368427e-8*(1.0 - cos(theta)**2)**3.5*(2635284526.875*cos(theta)**5 - 1145775881.25*cos(theta)**3 + 81841134.375*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl12_m_minus_6(theta, phi):
    return 6.68922506214776e-7*(1.0 - cos(theta)**2)**3*(439214087.8125*cos(theta)**6 - 286443970.3125*cos(theta)**4 + 40920567.1875*cos(theta)**2 - 717904.6875)*sin(6*phi)

#@torch.jit.script
def Yl12_m_minus_5(theta, phi):
    return 7.50863650967357e-6*(1.0 - cos(theta)**2)**2.5*(62744869.6875*cos(theta)**7 - 57288794.0625*cos(theta)**5 + 13640189.0625*cos(theta)**3 - 717904.6875*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl12_m_minus_4(theta, phi):
    return 8.75649965675714e-5*(1.0 - cos(theta)**2)**2*(7843108.7109375*cos(theta)**8 - 9548132.34375*cos(theta)**6 + 3410047.265625*cos(theta)**4 - 358952.34375*cos(theta)**2 + 5278.7109375)*sin(4*phi)

#@torch.jit.script
def Yl12_m_minus_3(theta, phi):
    return 0.00105077995881086*(1.0 - cos(theta)**2)**1.5*(871456.5234375*cos(theta)**9 - 1364018.90625*cos(theta)**7 + 682009.453125*cos(theta)**5 - 119650.78125*cos(theta)**3 + 5278.7109375*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl12_m_minus_2(theta, phi):
    return 0.0128693736551466*(1.0 - cos(theta)**2)*(87145.65234375*cos(theta)**10 - 170502.36328125*cos(theta)**8 + 113668.2421875*cos(theta)**6 - 29912.6953125*cos(theta)**4 + 2639.35546875*cos(theta)**2 - 35.19140625)*sin(2*phi)

#@torch.jit.script
def Yl12_m_minus_1(theta, phi):
    return 0.159704727088682*(1.0 - cos(theta)**2)**0.5*(7922.33203125*cos(theta)**11 - 18944.70703125*cos(theta)**9 + 16238.3203125*cos(theta)**7 - 5982.5390625*cos(theta)**5 + 879.78515625*cos(theta)**3 - 35.19140625*cos(theta))*sin(phi)

#@torch.jit.script
def Yl12_m0(theta, phi):
    return 2925.40998269608*cos(theta)**12 - 8394.65473295397*cos(theta)**10 + 8994.27292816496*cos(theta)**8 - 4418.23933313367*cos(theta)**6 + 974.611617603015*cos(theta)**4 - 77.9689294082412*cos(theta)**2 + 0.999601659080015

#@torch.jit.script
def Yl12_m1(theta, phi):
    return 0.159704727088682*(1.0 - cos(theta)**2)**0.5*(7922.33203125*cos(theta)**11 - 18944.70703125*cos(theta)**9 + 16238.3203125*cos(theta)**7 - 5982.5390625*cos(theta)**5 + 879.78515625*cos(theta)**3 - 35.19140625*cos(theta))*cos(phi)

#@torch.jit.script
def Yl12_m2(theta, phi):
    return 0.0128693736551466*(1.0 - cos(theta)**2)*(87145.65234375*cos(theta)**10 - 170502.36328125*cos(theta)**8 + 113668.2421875*cos(theta)**6 - 29912.6953125*cos(theta)**4 + 2639.35546875*cos(theta)**2 - 35.19140625)*cos(2*phi)

#@torch.jit.script
def Yl12_m3(theta, phi):
    return 0.00105077995881086*(1.0 - cos(theta)**2)**1.5*(871456.5234375*cos(theta)**9 - 1364018.90625*cos(theta)**7 + 682009.453125*cos(theta)**5 - 119650.78125*cos(theta)**3 + 5278.7109375*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl12_m4(theta, phi):
    return 8.75649965675714e-5*(1.0 - cos(theta)**2)**2*(7843108.7109375*cos(theta)**8 - 9548132.34375*cos(theta)**6 + 3410047.265625*cos(theta)**4 - 358952.34375*cos(theta)**2 + 5278.7109375)*cos(4*phi)

#@torch.jit.script
def Yl12_m5(theta, phi):
    return 7.50863650967357e-6*(1.0 - cos(theta)**2)**2.5*(62744869.6875*cos(theta)**7 - 57288794.0625*cos(theta)**5 + 13640189.0625*cos(theta)**3 - 717904.6875*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl12_m6(theta, phi):
    return 6.68922506214776e-7*(1.0 - cos(theta)**2)**3*(439214087.8125*cos(theta)**6 - 286443970.3125*cos(theta)**4 + 40920567.1875*cos(theta)**2 - 717904.6875)*cos(6*phi)

#@torch.jit.script
def Yl12_m7(theta, phi):
    return 6.26503328368427e-8*(1.0 - cos(theta)**2)**3.5*(2635284526.875*cos(theta)**5 - 1145775881.25*cos(theta)**3 + 81841134.375*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl12_m8(theta, phi):
    return 6.26503328368427e-9*(1.0 - cos(theta)**2)**4*(13176422634.375*cos(theta)**4 - 3437327643.75*cos(theta)**2 + 81841134.375)*cos(8*phi)

#@torch.jit.script
def Yl12_m9(theta, phi):
    return 6.83571172711927e-10*(1.0 - cos(theta)**2)**4.5*(52705690537.5*cos(theta)**3 - 6874655287.5*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl12_m10(theta, phi):
    return 8.4141794839602e-11*(1.0 - cos(theta)**2)**5*(158117071612.5*cos(theta)**2 - 6874655287.5)*cos(10*phi)

#@torch.jit.script
def Yl12_m11(theta, phi):
    return 3.92321052893598*(1.0 - cos(theta)**2)**5.5*cos(11*phi)*cos(theta)

#@torch.jit.script
def Yl12_m12(theta, phi):
    return 0.800821995783972*(1.0 - cos(theta)**2)**6*cos(12*phi)

#@torch.jit.script
def Yl13_m_minus_13(theta, phi):
    return 0.816077118837628*(1.0 - cos(theta)**2)**6.5*sin(13*phi)

#@torch.jit.script
def Yl13_m_minus_12(theta, phi):
    return 4.16119315354964*(1.0 - cos(theta)**2)**6*sin(12*phi)*cos(theta)

#@torch.jit.script
def Yl13_m_minus_11(theta, phi):
    return 3.72180924766049e-12*(1.0 - cos(theta)**2)**5.5*(3952926790312.5*cos(theta)**2 - 158117071612.5)*sin(11*phi)

#@torch.jit.script
def Yl13_m_minus_10(theta, phi):
    return 3.15805986876424e-11*(1.0 - cos(theta)**2)**5*(1317642263437.5*cos(theta)**3 - 158117071612.5*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl13_m_minus_9(theta, phi):
    return 3.02910461422567e-10*(1.0 - cos(theta)**2)**4.5*(329410565859.375*cos(theta)**4 - 79058535806.25*cos(theta)**2 + 1718663821.875)*sin(9*phi)

#@torch.jit.script
def Yl13_m_minus_8(theta, phi):
    return 3.17695172143292e-9*(1.0 - cos(theta)**2)**4*(65882113171.875*cos(theta)**5 - 26352845268.75*cos(theta)**3 + 1718663821.875*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl13_m_minus_7(theta, phi):
    return 3.5661194627771e-8*(1.0 - cos(theta)**2)**3.5*(10980352195.3125*cos(theta)**6 - 6588211317.1875*cos(theta)**4 + 859331910.9375*cos(theta)**2 - 13640189.0625)*sin(7*phi)

#@torch.jit.script
def Yl13_m_minus_6(theta, phi):
    return 4.21948945157073e-7*(1.0 - cos(theta)**2)**3*(1568621742.1875*cos(theta)**7 - 1317642263.4375*cos(theta)**5 + 286443970.3125*cos(theta)**3 - 13640189.0625*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl13_m_minus_5(theta, phi):
    return 5.2021359721285e-6*(1.0 - cos(theta)**2)**2.5*(196077717.773438*cos(theta)**8 - 219607043.90625*cos(theta)**6 + 71610992.578125*cos(theta)**4 - 6820094.53125*cos(theta)**2 + 89738.0859375)*sin(5*phi)

#@torch.jit.script
def Yl13_m_minus_4(theta, phi):
    return 6.62123812058377e-5*(1.0 - cos(theta)**2)**2*(21786413.0859375*cos(theta)**9 - 31372434.84375*cos(theta)**7 + 14322198.515625*cos(theta)**5 - 2273364.84375*cos(theta)**3 + 89738.0859375*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl13_m_minus_3(theta, phi):
    return 0.000863303829622583*(1.0 - cos(theta)**2)**1.5*(2178641.30859375*cos(theta)**10 - 3921554.35546875*cos(theta)**8 + 2387033.0859375*cos(theta)**6 - 568341.2109375*cos(theta)**4 + 44869.04296875*cos(theta)**2 - 527.87109375)*sin(3*phi)

#@torch.jit.script
def Yl13_m_minus_2(theta, phi):
    return 0.0114530195317401*(1.0 - cos(theta)**2)*(198058.30078125*cos(theta)**11 - 435728.26171875*cos(theta)**9 + 341004.7265625*cos(theta)**7 - 113668.2421875*cos(theta)**5 + 14956.34765625*cos(theta)**3 - 527.87109375*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl13_m_minus_1(theta, phi):
    return 0.153658381323621*(1.0 - cos(theta)**2)**0.5*(16504.8583984375*cos(theta)**12 - 43572.826171875*cos(theta)**10 + 42625.5908203125*cos(theta)**8 - 18944.70703125*cos(theta)**6 + 3739.0869140625*cos(theta)**4 - 263.935546875*cos(theta)**2 + 2.9326171875)*sin(phi)

#@torch.jit.script
def Yl13_m0(theta, phi):
    return 5846.49083422938*cos(theta)**13 - 18241.0514027957*cos(theta)**11 + 21809.9527642122*cos(theta)**9 - 12462.8301509784*cos(theta)**7 + 3443.67675224404*cos(theta)**5 - 405.138441440475*cos(theta)**3 + 13.5046147146825*cos(theta)

#@torch.jit.script
def Yl13_m1(theta, phi):
    return 0.153658381323621*(1.0 - cos(theta)**2)**0.5*(16504.8583984375*cos(theta)**12 - 43572.826171875*cos(theta)**10 + 42625.5908203125*cos(theta)**8 - 18944.70703125*cos(theta)**6 + 3739.0869140625*cos(theta)**4 - 263.935546875*cos(theta)**2 + 2.9326171875)*cos(phi)

#@torch.jit.script
def Yl13_m2(theta, phi):
    return 0.0114530195317401*(1.0 - cos(theta)**2)*(198058.30078125*cos(theta)**11 - 435728.26171875*cos(theta)**9 + 341004.7265625*cos(theta)**7 - 113668.2421875*cos(theta)**5 + 14956.34765625*cos(theta)**3 - 527.87109375*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl13_m3(theta, phi):
    return 0.000863303829622583*(1.0 - cos(theta)**2)**1.5*(2178641.30859375*cos(theta)**10 - 3921554.35546875*cos(theta)**8 + 2387033.0859375*cos(theta)**6 - 568341.2109375*cos(theta)**4 + 44869.04296875*cos(theta)**2 - 527.87109375)*cos(3*phi)

#@torch.jit.script
def Yl13_m4(theta, phi):
    return 6.62123812058377e-5*(1.0 - cos(theta)**2)**2*(21786413.0859375*cos(theta)**9 - 31372434.84375*cos(theta)**7 + 14322198.515625*cos(theta)**5 - 2273364.84375*cos(theta)**3 + 89738.0859375*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl13_m5(theta, phi):
    return 5.2021359721285e-6*(1.0 - cos(theta)**2)**2.5*(196077717.773438*cos(theta)**8 - 219607043.90625*cos(theta)**6 + 71610992.578125*cos(theta)**4 - 6820094.53125*cos(theta)**2 + 89738.0859375)*cos(5*phi)

#@torch.jit.script
def Yl13_m6(theta, phi):
    return 4.21948945157073e-7*(1.0 - cos(theta)**2)**3*(1568621742.1875*cos(theta)**7 - 1317642263.4375*cos(theta)**5 + 286443970.3125*cos(theta)**3 - 13640189.0625*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl13_m7(theta, phi):
    return 3.5661194627771e-8*(1.0 - cos(theta)**2)**3.5*(10980352195.3125*cos(theta)**6 - 6588211317.1875*cos(theta)**4 + 859331910.9375*cos(theta)**2 - 13640189.0625)*cos(7*phi)

#@torch.jit.script
def Yl13_m8(theta, phi):
    return 3.17695172143292e-9*(1.0 - cos(theta)**2)**4*(65882113171.875*cos(theta)**5 - 26352845268.75*cos(theta)**3 + 1718663821.875*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl13_m9(theta, phi):
    return 3.02910461422567e-10*(1.0 - cos(theta)**2)**4.5*(329410565859.375*cos(theta)**4 - 79058535806.25*cos(theta)**2 + 1718663821.875)*cos(9*phi)

#@torch.jit.script
def Yl13_m10(theta, phi):
    return 3.15805986876424e-11*(1.0 - cos(theta)**2)**5*(1317642263437.5*cos(theta)**3 - 158117071612.5*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl13_m11(theta, phi):
    return 3.72180924766049e-12*(1.0 - cos(theta)**2)**5.5*(3952926790312.5*cos(theta)**2 - 158117071612.5)*cos(11*phi)

#@torch.jit.script
def Yl13_m12(theta, phi):
    return 4.16119315354964*(1.0 - cos(theta)**2)**6*cos(12*phi)*cos(theta)

#@torch.jit.script
def Yl13_m13(theta, phi):
    return 0.816077118837628*(1.0 - cos(theta)**2)**6.5*cos(13*phi)

#@torch.jit.script
def Yl14_m_minus_14(theta, phi):
    return 0.830522083064524*(1.0 - cos(theta)**2)**7*sin(14*phi)

#@torch.jit.script
def Yl14_m_minus_13(theta, phi):
    return 4.39470978027212*(1.0 - cos(theta)**2)**6.5*sin(13*phi)*cos(theta)

#@torch.jit.script
def Yl14_m_minus_12(theta, phi):
    return 1.51291507116349e-13*(1.0 - cos(theta)**2)**6*(106729023338438.0*cos(theta)**2 - 3952926790312.5)*sin(12*phi)

#@torch.jit.script
def Yl14_m_minus_11(theta, phi):
    return 1.33617041195793e-12*(1.0 - cos(theta)**2)**5.5*(35576341112812.5*cos(theta)**3 - 3952926790312.5*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl14_m_minus_10(theta, phi):
    return 1.33617041195793e-11*(1.0 - cos(theta)**2)**5*(8894085278203.13*cos(theta)**4 - 1976463395156.25*cos(theta)**2 + 39529267903.125)*sin(10*phi)

#@torch.jit.script
def Yl14_m_minus_9(theta, phi):
    return 1.46370135060066e-10*(1.0 - cos(theta)**2)**4.5*(1778817055640.63*cos(theta)**5 - 658821131718.75*cos(theta)**3 + 39529267903.125*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl14_m_minus_8(theta, phi):
    return 1.71945976061531e-9*(1.0 - cos(theta)**2)**4*(296469509273.438*cos(theta)**6 - 164705282929.688*cos(theta)**4 + 19764633951.5625*cos(theta)**2 - 286443970.3125)*sin(8*phi)

#@torch.jit.script
def Yl14_m_minus_7(theta, phi):
    return 2.13379344766496e-8*(1.0 - cos(theta)**2)**3.5*(42352787039.0625*cos(theta)**7 - 32941056585.9375*cos(theta)**5 + 6588211317.1875*cos(theta)**3 - 286443970.3125*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl14_m_minus_6(theta, phi):
    return 2.76571240765567e-7*(1.0 - cos(theta)**2)**3*(5294098379.88281*cos(theta)**8 - 5490176097.65625*cos(theta)**6 + 1647052829.29688*cos(theta)**4 - 143221985.15625*cos(theta)**2 + 1705023.6328125)*sin(6*phi)

#@torch.jit.script
def Yl14_m_minus_5(theta, phi):
    return 3.71059256983961e-6*(1.0 - cos(theta)**2)**2.5*(588233153.320313*cos(theta)**9 - 784310871.09375*cos(theta)**7 + 329410565.859375*cos(theta)**5 - 47740661.71875*cos(theta)**3 + 1705023.6328125*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl14_m_minus_4(theta, phi):
    return 5.11469888818129e-5*(1.0 - cos(theta)**2)**2*(58823315.3320313*cos(theta)**10 - 98038858.8867188*cos(theta)**8 + 54901760.9765625*cos(theta)**6 - 11935165.4296875*cos(theta)**4 + 852511.81640625*cos(theta)**2 - 8973.80859375)*sin(4*phi)

#@torch.jit.script
def Yl14_m_minus_3(theta, phi):
    return 0.000719701928156307*(1.0 - cos(theta)**2)**1.5*(5347574.12109375*cos(theta)**11 - 10893206.5429688*cos(theta)**9 + 7843108.7109375*cos(theta)**7 - 2387033.0859375*cos(theta)**5 + 284170.60546875*cos(theta)**3 - 8973.80859375*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl14_m_minus_2(theta, phi):
    return 0.0102793996196251*(1.0 - cos(theta)**2)*(445631.176757813*cos(theta)**12 - 1089320.65429688*cos(theta)**10 + 980388.588867188*cos(theta)**8 - 397838.84765625*cos(theta)**6 + 71042.6513671875*cos(theta)**4 - 4486.904296875*cos(theta)**2 + 43.9892578125)*sin(2*phi)

#@torch.jit.script
def Yl14_m_minus_1(theta, phi):
    return 0.148251609638173*(1.0 - cos(theta)**2)**0.5*(34279.3212890625*cos(theta)**13 - 99029.150390625*cos(theta)**11 + 108932.065429688*cos(theta)**9 - 56834.12109375*cos(theta)**7 + 14208.5302734375*cos(theta)**5 - 1495.634765625*cos(theta)**3 + 43.9892578125*cos(theta))*sin(phi)

#@torch.jit.script
def Yl14_m0(theta, phi):
    return 11685.5220302715*cos(theta)**14 - 39384.5372131372*cos(theta)**12 + 51987.5891213411*cos(theta)**10 - 33904.9494269616*cos(theta)**8 + 11301.6498089872*cos(theta)**6 - 1784.47102247166*cos(theta)**4 + 104.968883674804*cos(theta)**2 - 0.99970365404575

#@torch.jit.script
def Yl14_m1(theta, phi):
    return 0.148251609638173*(1.0 - cos(theta)**2)**0.5*(34279.3212890625*cos(theta)**13 - 99029.150390625*cos(theta)**11 + 108932.065429688*cos(theta)**9 - 56834.12109375*cos(theta)**7 + 14208.5302734375*cos(theta)**5 - 1495.634765625*cos(theta)**3 + 43.9892578125*cos(theta))*cos(phi)

#@torch.jit.script
def Yl14_m2(theta, phi):
    return 0.0102793996196251*(1.0 - cos(theta)**2)*(445631.176757813*cos(theta)**12 - 1089320.65429688*cos(theta)**10 + 980388.588867188*cos(theta)**8 - 397838.84765625*cos(theta)**6 + 71042.6513671875*cos(theta)**4 - 4486.904296875*cos(theta)**2 + 43.9892578125)*cos(2*phi)

#@torch.jit.script
def Yl14_m3(theta, phi):
    return 0.000719701928156307*(1.0 - cos(theta)**2)**1.5*(5347574.12109375*cos(theta)**11 - 10893206.5429688*cos(theta)**9 + 7843108.7109375*cos(theta)**7 - 2387033.0859375*cos(theta)**5 + 284170.60546875*cos(theta)**3 - 8973.80859375*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl14_m4(theta, phi):
    return 5.11469888818129e-5*(1.0 - cos(theta)**2)**2*(58823315.3320313*cos(theta)**10 - 98038858.8867188*cos(theta)**8 + 54901760.9765625*cos(theta)**6 - 11935165.4296875*cos(theta)**4 + 852511.81640625*cos(theta)**2 - 8973.80859375)*cos(4*phi)

#@torch.jit.script
def Yl14_m5(theta, phi):
    return 3.71059256983961e-6*(1.0 - cos(theta)**2)**2.5*(588233153.320313*cos(theta)**9 - 784310871.09375*cos(theta)**7 + 329410565.859375*cos(theta)**5 - 47740661.71875*cos(theta)**3 + 1705023.6328125*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl14_m6(theta, phi):
    return 2.76571240765567e-7*(1.0 - cos(theta)**2)**3*(5294098379.88281*cos(theta)**8 - 5490176097.65625*cos(theta)**6 + 1647052829.29688*cos(theta)**4 - 143221985.15625*cos(theta)**2 + 1705023.6328125)*cos(6*phi)

#@torch.jit.script
def Yl14_m7(theta, phi):
    return 2.13379344766496e-8*(1.0 - cos(theta)**2)**3.5*(42352787039.0625*cos(theta)**7 - 32941056585.9375*cos(theta)**5 + 6588211317.1875*cos(theta)**3 - 286443970.3125*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl14_m8(theta, phi):
    return 1.71945976061531e-9*(1.0 - cos(theta)**2)**4*(296469509273.438*cos(theta)**6 - 164705282929.688*cos(theta)**4 + 19764633951.5625*cos(theta)**2 - 286443970.3125)*cos(8*phi)

#@torch.jit.script
def Yl14_m9(theta, phi):
    return 1.46370135060066e-10*(1.0 - cos(theta)**2)**4.5*(1778817055640.63*cos(theta)**5 - 658821131718.75*cos(theta)**3 + 39529267903.125*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl14_m10(theta, phi):
    return 1.33617041195793e-11*(1.0 - cos(theta)**2)**5*(8894085278203.13*cos(theta)**4 - 1976463395156.25*cos(theta)**2 + 39529267903.125)*cos(10*phi)

#@torch.jit.script
def Yl14_m11(theta, phi):
    return 1.33617041195793e-12*(1.0 - cos(theta)**2)**5.5*(35576341112812.5*cos(theta)**3 - 3952926790312.5*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl14_m12(theta, phi):
    return 1.51291507116349e-13*(1.0 - cos(theta)**2)**6*(106729023338438.0*cos(theta)**2 - 3952926790312.5)*cos(12*phi)

#@torch.jit.script
def Yl14_m13(theta, phi):
    return 4.39470978027212*(1.0 - cos(theta)**2)**6.5*cos(13*phi)*cos(theta)

#@torch.jit.script
def Yl14_m14(theta, phi):
    return 0.830522083064524*(1.0 - cos(theta)**2)**7*cos(14*phi)

#@torch.jit.script
def Yl15_m_minus_15(theta, phi):
    return 0.844250650857373*(1.0 - cos(theta)**2)**7.5*sin(15*phi)

#@torch.jit.script
def Yl15_m_minus_14(theta, phi):
    return 4.62415125663001*(1.0 - cos(theta)**2)**7*sin(14*phi)*cos(theta)

#@torch.jit.script
def Yl15_m_minus_13(theta, phi):
    return 5.68899431025918e-15*(1.0 - cos(theta)**2)**6.5*(3.09514167681469e+15*cos(theta)**2 - 106729023338438.0)*sin(13*phi)

#@torch.jit.script
def Yl15_m_minus_12(theta, phi):
    return 5.21404941098716e-14*(1.0 - cos(theta)**2)**6*(1.03171389227156e+15*cos(theta)**3 - 106729023338438.0*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl15_m_minus_11(theta, phi):
    return 5.4185990958026e-13*(1.0 - cos(theta)**2)**5.5*(257928473067891.0*cos(theta)**4 - 53364511669218.8*cos(theta)**2 + 988231697578.125)*sin(11*phi)

#@torch.jit.script
def Yl15_m_minus_10(theta, phi):
    return 6.17815352749854e-12*(1.0 - cos(theta)**2)**5*(51585694613578.1*cos(theta)**5 - 17788170556406.3*cos(theta)**3 + 988231697578.125*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl15_m_minus_9(theta, phi):
    return 7.56666184747369e-11*(1.0 - cos(theta)**2)**4.5*(8597615768929.69*cos(theta)**6 - 4447042639101.56*cos(theta)**4 + 494115848789.063*cos(theta)**2 - 6588211317.1875)*sin(9*phi)

#@torch.jit.script
def Yl15_m_minus_8(theta, phi):
    return 9.80751467720255e-10*(1.0 - cos(theta)**2)**4*(1228230824132.81*cos(theta)**7 - 889408527820.313*cos(theta)**5 + 164705282929.688*cos(theta)**3 - 6588211317.1875*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl15_m_minus_7(theta, phi):
    return 1.33035601710264e-8*(1.0 - cos(theta)**2)**3.5*(153528853016.602*cos(theta)**8 - 148234754636.719*cos(theta)**6 + 41176320732.4219*cos(theta)**4 - 3294105658.59375*cos(theta)**2 + 35805496.2890625)*sin(7*phi)

#@torch.jit.script
def Yl15_m_minus_6(theta, phi):
    return 1.87197684863824e-7*(1.0 - cos(theta)**2)**3*(17058761446.2891*cos(theta)**9 - 21176393519.5313*cos(theta)**7 + 8235264146.48438*cos(theta)**5 - 1098035219.53125*cos(theta)**3 + 35805496.2890625*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl15_m_minus_5(theta, phi):
    return 2.71275217737612e-6*(1.0 - cos(theta)**2)**2.5*(1705876144.62891*cos(theta)**10 - 2647049189.94141*cos(theta)**8 + 1372544024.41406*cos(theta)**6 - 274508804.882813*cos(theta)**4 + 17902748.1445313*cos(theta)**2 - 170502.36328125)*sin(5*phi)

#@torch.jit.script
def Yl15_m_minus_4(theta, phi):
    return 4.02366171874445e-5*(1.0 - cos(theta)**2)**2*(155079649.511719*cos(theta)**11 - 294116576.660156*cos(theta)**9 + 196077717.773438*cos(theta)**7 - 54901760.9765625*cos(theta)**5 + 5967582.71484375*cos(theta)**3 - 170502.36328125*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl15_m_minus_3(theta, phi):
    return 0.000607559596001151*(1.0 - cos(theta)**2)**1.5*(12923304.1259766*cos(theta)**12 - 29411657.6660156*cos(theta)**10 + 24509714.7216797*cos(theta)**8 - 9150293.49609375*cos(theta)**6 + 1491895.67871094*cos(theta)**4 - 85251.181640625*cos(theta)**2 + 747.8173828125)*sin(3*phi)

#@torch.jit.script
def Yl15_m_minus_2(theta, phi):
    return 0.00929387470704126*(1.0 - cos(theta)**2)*(994100.317382813*cos(theta)**13 - 2673787.06054688*cos(theta)**11 + 2723301.63574219*cos(theta)**9 - 1307184.78515625*cos(theta)**7 + 298379.135742188*cos(theta)**5 - 28417.060546875*cos(theta)**3 + 747.8173828125*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl15_m_minus_1(theta, phi):
    return 0.143378915753688*(1.0 - cos(theta)**2)**0.5*(71007.1655273438*cos(theta)**14 - 222815.588378906*cos(theta)**12 + 272330.163574219*cos(theta)**10 - 163398.098144531*cos(theta)**8 + 49729.8559570313*cos(theta)**6 - 7104.26513671875*cos(theta)**4 + 373.90869140625*cos(theta)**2 - 3.14208984375)*sin(phi)

#@torch.jit.script
def Yl15_m0(theta, phi):
    return 23358.0565385283*cos(theta)**15 - 84572.2736739818*cos(theta)**13 + 122159.950862418*cos(theta)**11 - 89583.9639657733*cos(theta)**9 + 35054.5945953026*cos(theta)**7 - 7010.91891906052*cos(theta)**5 + 614.992887636888*cos(theta)**3 - 15.5040223774005*cos(theta)

#@torch.jit.script
def Yl15_m1(theta, phi):
    return 0.143378915753688*(1.0 - cos(theta)**2)**0.5*(71007.1655273438*cos(theta)**14 - 222815.588378906*cos(theta)**12 + 272330.163574219*cos(theta)**10 - 163398.098144531*cos(theta)**8 + 49729.8559570313*cos(theta)**6 - 7104.26513671875*cos(theta)**4 + 373.90869140625*cos(theta)**2 - 3.14208984375)*cos(phi)

#@torch.jit.script
def Yl15_m2(theta, phi):
    return 0.00929387470704126*(1.0 - cos(theta)**2)*(994100.317382813*cos(theta)**13 - 2673787.06054688*cos(theta)**11 + 2723301.63574219*cos(theta)**9 - 1307184.78515625*cos(theta)**7 + 298379.135742188*cos(theta)**5 - 28417.060546875*cos(theta)**3 + 747.8173828125*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl15_m3(theta, phi):
    return 0.000607559596001151*(1.0 - cos(theta)**2)**1.5*(12923304.1259766*cos(theta)**12 - 29411657.6660156*cos(theta)**10 + 24509714.7216797*cos(theta)**8 - 9150293.49609375*cos(theta)**6 + 1491895.67871094*cos(theta)**4 - 85251.181640625*cos(theta)**2 + 747.8173828125)*cos(3*phi)

#@torch.jit.script
def Yl15_m4(theta, phi):
    return 4.02366171874445e-5*(1.0 - cos(theta)**2)**2*(155079649.511719*cos(theta)**11 - 294116576.660156*cos(theta)**9 + 196077717.773438*cos(theta)**7 - 54901760.9765625*cos(theta)**5 + 5967582.71484375*cos(theta)**3 - 170502.36328125*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl15_m5(theta, phi):
    return 2.71275217737612e-6*(1.0 - cos(theta)**2)**2.5*(1705876144.62891*cos(theta)**10 - 2647049189.94141*cos(theta)**8 + 1372544024.41406*cos(theta)**6 - 274508804.882813*cos(theta)**4 + 17902748.1445313*cos(theta)**2 - 170502.36328125)*cos(5*phi)

#@torch.jit.script
def Yl15_m6(theta, phi):
    return 1.87197684863824e-7*(1.0 - cos(theta)**2)**3*(17058761446.2891*cos(theta)**9 - 21176393519.5313*cos(theta)**7 + 8235264146.48438*cos(theta)**5 - 1098035219.53125*cos(theta)**3 + 35805496.2890625*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl15_m7(theta, phi):
    return 1.33035601710264e-8*(1.0 - cos(theta)**2)**3.5*(153528853016.602*cos(theta)**8 - 148234754636.719*cos(theta)**6 + 41176320732.4219*cos(theta)**4 - 3294105658.59375*cos(theta)**2 + 35805496.2890625)*cos(7*phi)

#@torch.jit.script
def Yl15_m8(theta, phi):
    return 9.80751467720255e-10*(1.0 - cos(theta)**2)**4*(1228230824132.81*cos(theta)**7 - 889408527820.313*cos(theta)**5 + 164705282929.688*cos(theta)**3 - 6588211317.1875*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl15_m9(theta, phi):
    return 7.56666184747369e-11*(1.0 - cos(theta)**2)**4.5*(8597615768929.69*cos(theta)**6 - 4447042639101.56*cos(theta)**4 + 494115848789.063*cos(theta)**2 - 6588211317.1875)*cos(9*phi)

#@torch.jit.script
def Yl15_m10(theta, phi):
    return 6.17815352749854e-12*(1.0 - cos(theta)**2)**5*(51585694613578.1*cos(theta)**5 - 17788170556406.3*cos(theta)**3 + 988231697578.125*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl15_m11(theta, phi):
    return 5.4185990958026e-13*(1.0 - cos(theta)**2)**5.5*(257928473067891.0*cos(theta)**4 - 53364511669218.8*cos(theta)**2 + 988231697578.125)*cos(11*phi)

#@torch.jit.script
def Yl15_m12(theta, phi):
    return 5.21404941098716e-14*(1.0 - cos(theta)**2)**6*(1.03171389227156e+15*cos(theta)**3 - 106729023338438.0*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl15_m13(theta, phi):
    return 5.68899431025918e-15*(1.0 - cos(theta)**2)**6.5*(3.09514167681469e+15*cos(theta)**2 - 106729023338438.0)*cos(13*phi)

#@torch.jit.script
def Yl15_m14(theta, phi):
    return 4.62415125663001*(1.0 - cos(theta)**2)**7*cos(14*phi)*cos(theta)

#@torch.jit.script
def Yl15_m15(theta, phi):
    return 0.844250650857373*(1.0 - cos(theta)**2)**7.5*cos(15*phi)

#@torch.jit.script
def Yl16_m_minus_16(theta, phi):
    return 0.857340588838025*(1.0 - cos(theta)**2)**8*sin(16*phi)

#@torch.jit.script
def Yl16_m_minus_15(theta, phi):
    return 4.84985075323068*(1.0 - cos(theta)**2)**7.5*sin(15*phi)*cos(theta)

#@torch.jit.script
def Yl16_m_minus_14(theta, phi):
    return 1.98999505000411e-16*(1.0 - cos(theta)**2)**7*(9.59493919812553e+16*cos(theta)**2 - 3.09514167681469e+15)*sin(14*phi)

#@torch.jit.script
def Yl16_m_minus_13(theta, phi):
    return 1.8878750671421e-15*(1.0 - cos(theta)**2)**6.5*(3.19831306604184e+16*cos(theta)**3 - 3.09514167681469e+15*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl16_m_minus_12(theta, phi):
    return 2.03330367436807e-14*(1.0 - cos(theta)**2)**6*(7.99578266510461e+15*cos(theta)**4 - 1.54757083840734e+15*cos(theta)**2 + 26682255834609.4)*sin(12*phi)

#@torch.jit.script
def Yl16_m_minus_11(theta, phi):
    return 2.40583735216622e-13*(1.0 - cos(theta)**2)**5.5*(1.59915653302092e+15*cos(theta)**5 - 515856946135781.0*cos(theta)**3 + 26682255834609.4*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl16_m_minus_10(theta, phi):
    return 3.06213103106751e-12*(1.0 - cos(theta)**2)**5*(266526088836820.0*cos(theta)**6 - 128964236533945.0*cos(theta)**4 + 13341127917304.7*cos(theta)**2 - 164705282929.688)*sin(10*phi)

#@torch.jit.script
def Yl16_m_minus_9(theta, phi):
    return 4.1310406124361e-11*(1.0 - cos(theta)**2)**4.5*(38075155548117.2*cos(theta)**7 - 25792847306789.1*cos(theta)**5 + 4447042639101.56*cos(theta)**3 - 164705282929.688*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl16_m_minus_8(theta, phi):
    return 5.84217366082119e-10*(1.0 - cos(theta)**2)**4*(4759394443514.65*cos(theta)**8 - 4298807884464.84*cos(theta)**6 + 1111760659775.39*cos(theta)**4 - 82352641464.8438*cos(theta)**2 + 823526414.648438)*sin(8*phi)

#@torch.jit.script
def Yl16_m_minus_7(theta, phi):
    return 8.58620667464373e-9*(1.0 - cos(theta)**2)**3.5*(528821604834.961*cos(theta)**9 - 614115412066.406*cos(theta)**7 + 222352131955.078*cos(theta)**5 - 27450880488.2813*cos(theta)**3 + 823526414.648438*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl16_m_minus_6(theta, phi):
    return 1.30216271501415e-7*(1.0 - cos(theta)**2)**3*(52882160483.4961*cos(theta)**10 - 76764426508.3008*cos(theta)**8 + 37058688659.1797*cos(theta)**6 - 6862720122.07031*cos(theta)**4 + 411763207.324219*cos(theta)**2 - 3580549.62890625)*sin(6*phi)

#@torch.jit.script
def Yl16_m_minus_5(theta, phi):
    return 2.02568978918854e-6*(1.0 - cos(theta)**2)**2.5*(4807469134.86328*cos(theta)**11 - 8529380723.14453*cos(theta)**9 + 5294098379.88281*cos(theta)**7 - 1372544024.41406*cos(theta)**5 + 137254402.441406*cos(theta)**3 - 3580549.62890625*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl16_m_minus_4(theta, phi):
    return 3.21568284933344e-5*(1.0 - cos(theta)**2)**2*(400622427.905273*cos(theta)**12 - 852938072.314453*cos(theta)**10 + 661762297.485352*cos(theta)**8 - 228757337.402344*cos(theta)**6 + 34313600.6103516*cos(theta)**4 - 1790274.81445313*cos(theta)**2 + 14208.5302734375)*sin(4*phi)

#@torch.jit.script
def Yl16_m_minus_3(theta, phi):
    return 0.000518513279362185*(1.0 - cos(theta)**2)**1.5*(30817109.8388672*cos(theta)**13 - 77539824.7558594*cos(theta)**11 + 73529144.1650391*cos(theta)**9 - 32679619.6289063*cos(theta)**7 + 6862720.12207031*cos(theta)**5 - 596758.271484375*cos(theta)**3 + 14208.5302734375*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl16_m_minus_2(theta, phi):
    return 0.00845669566395355*(1.0 - cos(theta)**2)*(2201222.13134766*cos(theta)**14 - 6461652.06298828*cos(theta)**12 + 7352914.41650391*cos(theta)**10 - 4084952.45361328*cos(theta)**8 + 1143786.68701172*cos(theta)**6 - 149189.567871094*cos(theta)**4 + 7104.26513671875*cos(theta)**2 - 53.41552734375)*sin(2*phi)

#@torch.jit.script
def Yl16_m_minus_1(theta, phi):
    return 0.138957689313105*(1.0 - cos(theta)**2)**0.5*(146748.142089844*cos(theta)**15 - 497050.158691406*cos(theta)**13 + 668446.765136719*cos(theta)**11 - 453883.605957031*cos(theta)**9 + 163398.098144531*cos(theta)**7 - 29837.9135742188*cos(theta)**5 + 2368.08837890625*cos(theta)**3 - 53.41552734375*cos(theta))*sin(phi)

#@torch.jit.script
def Yl16_m0(theta, phi):
    return 46693.2969032527*cos(theta)**16 - 180748.246077107*cos(theta)**14 + 283587.76539684*cos(theta)**12 - 231071.512545574*cos(theta)**10 + 103982.180645508*cos(theta)**8 - 25317.4005049933*cos(theta)**6 + 3013.97625059444*cos(theta)**4 - 135.968853410275*cos(theta)**2 + 0.999770980957908

#@torch.jit.script
def Yl16_m1(theta, phi):
    return 0.138957689313105*(1.0 - cos(theta)**2)**0.5*(146748.142089844*cos(theta)**15 - 497050.158691406*cos(theta)**13 + 668446.765136719*cos(theta)**11 - 453883.605957031*cos(theta)**9 + 163398.098144531*cos(theta)**7 - 29837.9135742188*cos(theta)**5 + 2368.08837890625*cos(theta)**3 - 53.41552734375*cos(theta))*cos(phi)

#@torch.jit.script
def Yl16_m2(theta, phi):
    return 0.00845669566395355*(1.0 - cos(theta)**2)*(2201222.13134766*cos(theta)**14 - 6461652.06298828*cos(theta)**12 + 7352914.41650391*cos(theta)**10 - 4084952.45361328*cos(theta)**8 + 1143786.68701172*cos(theta)**6 - 149189.567871094*cos(theta)**4 + 7104.26513671875*cos(theta)**2 - 53.41552734375)*cos(2*phi)

#@torch.jit.script
def Yl16_m3(theta, phi):
    return 0.000518513279362185*(1.0 - cos(theta)**2)**1.5*(30817109.8388672*cos(theta)**13 - 77539824.7558594*cos(theta)**11 + 73529144.1650391*cos(theta)**9 - 32679619.6289063*cos(theta)**7 + 6862720.12207031*cos(theta)**5 - 596758.271484375*cos(theta)**3 + 14208.5302734375*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl16_m4(theta, phi):
    return 3.21568284933344e-5*(1.0 - cos(theta)**2)**2*(400622427.905273*cos(theta)**12 - 852938072.314453*cos(theta)**10 + 661762297.485352*cos(theta)**8 - 228757337.402344*cos(theta)**6 + 34313600.6103516*cos(theta)**4 - 1790274.81445313*cos(theta)**2 + 14208.5302734375)*cos(4*phi)

#@torch.jit.script
def Yl16_m5(theta, phi):
    return 2.02568978918854e-6*(1.0 - cos(theta)**2)**2.5*(4807469134.86328*cos(theta)**11 - 8529380723.14453*cos(theta)**9 + 5294098379.88281*cos(theta)**7 - 1372544024.41406*cos(theta)**5 + 137254402.441406*cos(theta)**3 - 3580549.62890625*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl16_m6(theta, phi):
    return 1.30216271501415e-7*(1.0 - cos(theta)**2)**3*(52882160483.4961*cos(theta)**10 - 76764426508.3008*cos(theta)**8 + 37058688659.1797*cos(theta)**6 - 6862720122.07031*cos(theta)**4 + 411763207.324219*cos(theta)**2 - 3580549.62890625)*cos(6*phi)

#@torch.jit.script
def Yl16_m7(theta, phi):
    return 8.58620667464373e-9*(1.0 - cos(theta)**2)**3.5*(528821604834.961*cos(theta)**9 - 614115412066.406*cos(theta)**7 + 222352131955.078*cos(theta)**5 - 27450880488.2813*cos(theta)**3 + 823526414.648438*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl16_m8(theta, phi):
    return 5.84217366082119e-10*(1.0 - cos(theta)**2)**4*(4759394443514.65*cos(theta)**8 - 4298807884464.84*cos(theta)**6 + 1111760659775.39*cos(theta)**4 - 82352641464.8438*cos(theta)**2 + 823526414.648438)*cos(8*phi)

#@torch.jit.script
def Yl16_m9(theta, phi):
    return 4.1310406124361e-11*(1.0 - cos(theta)**2)**4.5*(38075155548117.2*cos(theta)**7 - 25792847306789.1*cos(theta)**5 + 4447042639101.56*cos(theta)**3 - 164705282929.688*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl16_m10(theta, phi):
    return 3.06213103106751e-12*(1.0 - cos(theta)**2)**5*(266526088836820.0*cos(theta)**6 - 128964236533945.0*cos(theta)**4 + 13341127917304.7*cos(theta)**2 - 164705282929.688)*cos(10*phi)

#@torch.jit.script
def Yl16_m11(theta, phi):
    return 2.40583735216622e-13*(1.0 - cos(theta)**2)**5.5*(1.59915653302092e+15*cos(theta)**5 - 515856946135781.0*cos(theta)**3 + 26682255834609.4*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl16_m12(theta, phi):
    return 2.03330367436807e-14*(1.0 - cos(theta)**2)**6*(7.99578266510461e+15*cos(theta)**4 - 1.54757083840734e+15*cos(theta)**2 + 26682255834609.4)*cos(12*phi)

#@torch.jit.script
def Yl16_m13(theta, phi):
    return 1.8878750671421e-15*(1.0 - cos(theta)**2)**6.5*(3.19831306604184e+16*cos(theta)**3 - 3.09514167681469e+15*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl16_m14(theta, phi):
    return 1.98999505000411e-16*(1.0 - cos(theta)**2)**7*(9.59493919812553e+16*cos(theta)**2 - 3.09514167681469e+15)*cos(14*phi)

#@torch.jit.script
def Yl16_m15(theta, phi):
    return 4.84985075323068*(1.0 - cos(theta)**2)**7.5*cos(15*phi)*cos(theta)

#@torch.jit.script
def Yl16_m16(theta, phi):
    return 0.857340588838025*(1.0 - cos(theta)**2)**8*cos(16*phi)

#@torch.jit.script
def Yl17_m_minus_17(theta, phi):
    return 0.869857171920628*(1.0 - cos(theta)**2)**8.5*sin(17*phi)

#@torch.jit.script
def Yl17_m_minus_16(theta, phi):
    return 5.07209532485536*(1.0 - cos(theta)**2)**8*sin(16*phi)*cos(theta)

#@torch.jit.script
def Yl17_m_minus_15(theta, phi):
    return 6.50688621401289e-18*(1.0 - cos(theta)**2)**7.5*(3.16632993538143e+18*cos(theta)**2 - 9.59493919812553e+16)*sin(15*phi)

#@torch.jit.script
def Yl17_m_minus_14(theta, phi):
    return 6.37542041547274e-17*(1.0 - cos(theta)**2)**7*(1.05544331179381e+18*cos(theta)**3 - 9.59493919812553e+16*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl17_m_minus_13(theta, phi):
    return 7.09936771746562e-16*(1.0 - cos(theta)**2)**6.5*(2.63860827948452e+17*cos(theta)**4 - 4.79746959906277e+16*cos(theta)**2 + 773785419203672.0)*sin(13*phi)

#@torch.jit.script
def Yl17_m_minus_12(theta, phi):
    return 8.69491420208903e-15*(1.0 - cos(theta)**2)**6*(5.27721655896904e+16*cos(theta)**5 - 1.59915653302092e+16*cos(theta)**3 + 773785419203672.0*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl17_m_minus_11(theta, phi):
    return 1.14693795555008e-13*(1.0 - cos(theta)**2)**5.5*(8.79536093161507e+15*cos(theta)**6 - 3.9978913325523e+15*cos(theta)**4 + 386892709601836.0*cos(theta)**2 - 4447042639101.56)*sin(11*phi)

#@torch.jit.script
def Yl17_m_minus_10(theta, phi):
    return 1.60571313777011e-12*(1.0 - cos(theta)**2)**5*(1.25648013308787e+15*cos(theta)**7 - 799578266510461.0*cos(theta)**5 + 128964236533945.0*cos(theta)**3 - 4447042639101.56*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl17_m_minus_9(theta, phi):
    return 2.35990671649205e-11*(1.0 - cos(theta)**2)**4.5*(157060016635983.0*cos(theta)**8 - 133263044418410.0*cos(theta)**6 + 32241059133486.3*cos(theta)**4 - 2223521319550.78*cos(theta)**2 + 20588160366.2109)*sin(9*phi)

#@torch.jit.script
def Yl17_m_minus_8(theta, phi):
    return 3.60996311929549e-10*(1.0 - cos(theta)**2)**4*(17451112959553.7*cos(theta)**9 - 19037577774058.6*cos(theta)**7 + 6448211826697.27*cos(theta)**5 - 741173773183.594*cos(theta)**3 + 20588160366.2109*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl17_m_minus_7(theta, phi):
    return 5.70785286308994e-9*(1.0 - cos(theta)**2)**3.5*(1745111295955.37*cos(theta)**10 - 2379697221757.32*cos(theta)**8 + 1074701971116.21*cos(theta)**6 - 185293443295.898*cos(theta)**4 + 10294080183.1055*cos(theta)**2 - 82352641.4648438)*sin(7*phi)

#@torch.jit.script
def Yl17_m_minus_6(theta, phi):
    return 9.2741631735508e-8*(1.0 - cos(theta)**2)**3*(158646481450.488*cos(theta)**11 - 264410802417.48*cos(theta)**9 + 153528853016.602*cos(theta)**7 - 37058688659.1797*cos(theta)**5 + 3431360061.03516*cos(theta)**3 - 82352641.4648438*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl17_m_minus_5(theta, phi):
    return 1.54073970252026e-6*(1.0 - cos(theta)**2)**2.5*(13220540120.874*cos(theta)**12 - 26441080241.748*cos(theta)**10 + 19191106627.0752*cos(theta)**8 - 6176448109.86328*cos(theta)**6 + 857840015.258789*cos(theta)**4 - 41176320.7324219*cos(theta)**2 + 298379.135742188)*sin(5*phi)

#@torch.jit.script
def Yl17_m_minus_4(theta, phi):
    return 2.6056272673653e-5*(1.0 - cos(theta)**2)**2*(1016964624.68262*cos(theta)**13 - 2403734567.43164*cos(theta)**11 + 2132345180.78613*cos(theta)**9 - 882349729.980469*cos(theta)**7 + 171568003.051758*cos(theta)**5 - 13725440.2441406*cos(theta)**3 + 298379.135742188*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl17_m_minus_3(theta, phi):
    return 0.000446772008544923*(1.0 - cos(theta)**2)**1.5*(72640330.3344727*cos(theta)**14 - 200311213.952637*cos(theta)**12 + 213234518.078613*cos(theta)**10 - 110293716.247559*cos(theta)**8 + 28594667.175293*cos(theta)**6 - 3431360.06103516*cos(theta)**4 + 149189.567871094*cos(theta)**2 - 1014.89501953125)*sin(3*phi)

#@torch.jit.script
def Yl17_m_minus_2(theta, phi):
    return 0.00773831818199403*(1.0 - cos(theta)**2)*(4842688.68896484*cos(theta)**15 - 15408554.9194336*cos(theta)**13 + 19384956.1889648*cos(theta)**11 - 12254857.3608398*cos(theta)**9 + 4084952.45361328*cos(theta)**7 - 686272.012207031*cos(theta)**5 + 49729.8559570313*cos(theta)**3 - 1014.89501953125*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl17_m_minus_1(theta, phi):
    return 0.134922187793101*(1.0 - cos(theta)**2)**0.5*(302668.043060303*cos(theta)**16 - 1100611.06567383*cos(theta)**14 + 1615413.01574707*cos(theta)**12 - 1225485.73608398*cos(theta)**10 + 510619.05670166*cos(theta)**8 - 114378.668701172*cos(theta)**6 + 12432.4639892578*cos(theta)**4 - 507.447509765625*cos(theta)**2 + 3.33847045898438)*sin(phi)

#@torch.jit.script
def Yl17_m0(theta, phi):
    return 93346.192942055*cos(theta)**17 - 384699.461821802*cos(theta)**15 + 651507.15308531*cos(theta)**13 - 584109.86138683*cos(theta)**11 + 297463.355335886*cos(theta)**9 - 85669.4463367351*cos(theta)**7 + 13036.6548773292*cos(theta)**5 - 886.847270566616*cos(theta)**3 + 17.5035645506569*cos(theta)

#@torch.jit.script
def Yl17_m1(theta, phi):
    return 0.134922187793101*(1.0 - cos(theta)**2)**0.5*(302668.043060303*cos(theta)**16 - 1100611.06567383*cos(theta)**14 + 1615413.01574707*cos(theta)**12 - 1225485.73608398*cos(theta)**10 + 510619.05670166*cos(theta)**8 - 114378.668701172*cos(theta)**6 + 12432.4639892578*cos(theta)**4 - 507.447509765625*cos(theta)**2 + 3.33847045898438)*cos(phi)

#@torch.jit.script
def Yl17_m2(theta, phi):
    return 0.00773831818199403*(1.0 - cos(theta)**2)*(4842688.68896484*cos(theta)**15 - 15408554.9194336*cos(theta)**13 + 19384956.1889648*cos(theta)**11 - 12254857.3608398*cos(theta)**9 + 4084952.45361328*cos(theta)**7 - 686272.012207031*cos(theta)**5 + 49729.8559570313*cos(theta)**3 - 1014.89501953125*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl17_m3(theta, phi):
    return 0.000446772008544923*(1.0 - cos(theta)**2)**1.5*(72640330.3344727*cos(theta)**14 - 200311213.952637*cos(theta)**12 + 213234518.078613*cos(theta)**10 - 110293716.247559*cos(theta)**8 + 28594667.175293*cos(theta)**6 - 3431360.06103516*cos(theta)**4 + 149189.567871094*cos(theta)**2 - 1014.89501953125)*cos(3*phi)

#@torch.jit.script
def Yl17_m4(theta, phi):
    return 2.6056272673653e-5*(1.0 - cos(theta)**2)**2*(1016964624.68262*cos(theta)**13 - 2403734567.43164*cos(theta)**11 + 2132345180.78613*cos(theta)**9 - 882349729.980469*cos(theta)**7 + 171568003.051758*cos(theta)**5 - 13725440.2441406*cos(theta)**3 + 298379.135742188*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl17_m5(theta, phi):
    return 1.54073970252026e-6*(1.0 - cos(theta)**2)**2.5*(13220540120.874*cos(theta)**12 - 26441080241.748*cos(theta)**10 + 19191106627.0752*cos(theta)**8 - 6176448109.86328*cos(theta)**6 + 857840015.258789*cos(theta)**4 - 41176320.7324219*cos(theta)**2 + 298379.135742188)*cos(5*phi)

#@torch.jit.script
def Yl17_m6(theta, phi):
    return 9.2741631735508e-8*(1.0 - cos(theta)**2)**3*(158646481450.488*cos(theta)**11 - 264410802417.48*cos(theta)**9 + 153528853016.602*cos(theta)**7 - 37058688659.1797*cos(theta)**5 + 3431360061.03516*cos(theta)**3 - 82352641.4648438*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl17_m7(theta, phi):
    return 5.70785286308994e-9*(1.0 - cos(theta)**2)**3.5*(1745111295955.37*cos(theta)**10 - 2379697221757.32*cos(theta)**8 + 1074701971116.21*cos(theta)**6 - 185293443295.898*cos(theta)**4 + 10294080183.1055*cos(theta)**2 - 82352641.4648438)*cos(7*phi)

#@torch.jit.script
def Yl17_m8(theta, phi):
    return 3.60996311929549e-10*(1.0 - cos(theta)**2)**4*(17451112959553.7*cos(theta)**9 - 19037577774058.6*cos(theta)**7 + 6448211826697.27*cos(theta)**5 - 741173773183.594*cos(theta)**3 + 20588160366.2109*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl17_m9(theta, phi):
    return 2.35990671649205e-11*(1.0 - cos(theta)**2)**4.5*(157060016635983.0*cos(theta)**8 - 133263044418410.0*cos(theta)**6 + 32241059133486.3*cos(theta)**4 - 2223521319550.78*cos(theta)**2 + 20588160366.2109)*cos(9*phi)

#@torch.jit.script
def Yl17_m10(theta, phi):
    return 1.60571313777011e-12*(1.0 - cos(theta)**2)**5*(1.25648013308787e+15*cos(theta)**7 - 799578266510461.0*cos(theta)**5 + 128964236533945.0*cos(theta)**3 - 4447042639101.56*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl17_m11(theta, phi):
    return 1.14693795555008e-13*(1.0 - cos(theta)**2)**5.5*(8.79536093161507e+15*cos(theta)**6 - 3.9978913325523e+15*cos(theta)**4 + 386892709601836.0*cos(theta)**2 - 4447042639101.56)*cos(11*phi)

#@torch.jit.script
def Yl17_m12(theta, phi):
    return 8.69491420208903e-15*(1.0 - cos(theta)**2)**6*(5.27721655896904e+16*cos(theta)**5 - 1.59915653302092e+16*cos(theta)**3 + 773785419203672.0*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl17_m13(theta, phi):
    return 7.09936771746562e-16*(1.0 - cos(theta)**2)**6.5*(2.63860827948452e+17*cos(theta)**4 - 4.79746959906277e+16*cos(theta)**2 + 773785419203672.0)*cos(13*phi)

#@torch.jit.script
def Yl17_m14(theta, phi):
    return 6.37542041547274e-17*(1.0 - cos(theta)**2)**7*(1.05544331179381e+18*cos(theta)**3 - 9.59493919812553e+16*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl17_m15(theta, phi):
    return 6.50688621401289e-18*(1.0 - cos(theta)**2)**7.5*(3.16632993538143e+18*cos(theta)**2 - 9.59493919812553e+16)*cos(15*phi)

#@torch.jit.script
def Yl17_m16(theta, phi):
    return 5.07209532485536*(1.0 - cos(theta)**2)**8*cos(16*phi)*cos(theta)

#@torch.jit.script
def Yl17_m17(theta, phi):
    return 0.869857171920628*(1.0 - cos(theta)**2)**8.5*cos(17*phi)

#@torch.jit.script
def Yl18_m_minus_18(theta, phi):
    return 0.881855768678329*(1.0 - cos(theta)**2)**9*sin(18*phi)

#@torch.jit.script
def Yl18_m_minus_17(theta, phi):
    return 5.29113461206997*(1.0 - cos(theta)**2)**8.5*sin(17*phi)*cos(theta)

#@torch.jit.script
def Yl18_m_minus_16(theta, phi):
    return 1.99730147939357e-19*(1.0 - cos(theta)**2)**8*(1.1082154773835e+20*cos(theta)**2 - 3.16632993538143e+18)*sin(16*phi)

#@torch.jit.script
def Yl18_m_minus_15(theta, phi):
    return 2.01717561545333e-18*(1.0 - cos(theta)**2)**7.5*(3.69405159127833e+19*cos(theta)**3 - 3.16632993538143e+18*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl18_m_minus_14(theta, phi):
    return 2.31755833840811e-17*(1.0 - cos(theta)**2)**7*(9.23512897819582e+18*cos(theta)**4 - 1.58316496769071e+18*cos(theta)**2 + 2.39873479953138e+16)*sin(14*phi)

#@torch.jit.script
def Yl18_m_minus_13(theta, phi):
    return 2.93150518387396e-16*(1.0 - cos(theta)**2)**6.5*(1.84702579563916e+18*cos(theta)**5 - 5.27721655896904e+17*cos(theta)**3 + 2.39873479953138e+16*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl18_m_minus_12(theta, phi):
    return 3.9980400343329e-15*(1.0 - cos(theta)**2)**6*(3.07837632606527e+17*cos(theta)**6 - 1.31930413974226e+17*cos(theta)**4 + 1.19936739976569e+16*cos(theta)**2 - 128964236533945.0)*sin(12*phi)

#@torch.jit.script
def Yl18_m_minus_11(theta, phi):
    return 5.79371043838662e-14*(1.0 - cos(theta)**2)**5.5*(4.39768046580754e+16*cos(theta)**7 - 2.63860827948452e+16*cos(theta)**5 + 3.9978913325523e+15*cos(theta)**3 - 128964236533945.0*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl18_m_minus_10(theta, phi):
    return 8.82471682796557e-13*(1.0 - cos(theta)**2)**5*(5.49710058225942e+15*cos(theta)**8 - 4.39768046580754e+15*cos(theta)**6 + 999472833138076.0*cos(theta)**4 - 64482118266972.7*cos(theta)**2 + 555880329887.695)*sin(10*phi)

#@torch.jit.script
def Yl18_m_minus_9(theta, phi):
    return 1.40088036704182e-11*(1.0 - cos(theta)**2)**4.5*(610788953584380.0*cos(theta)**9 - 628240066543934.0*cos(theta)**7 + 199894566627615.0*cos(theta)**5 - 21494039422324.2*cos(theta)**3 + 555880329887.695*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl18_m_minus_8(theta, phi):
    return 2.30188133218476e-10*(1.0 - cos(theta)**2)**4*(61078895358438.0*cos(theta)**10 - 78530008317991.7*cos(theta)**8 + 33315761104602.5*cos(theta)**6 - 5373509855581.05*cos(theta)**4 + 277940164943.848*cos(theta)**2 - 2058816036.62109)*sin(8*phi)

#@torch.jit.script
def Yl18_m_minus_7(theta, phi):
    return 3.8928345622358e-9*(1.0 - cos(theta)**2)**3.5*(5552626850767.09*cos(theta)**11 - 8725556479776.86*cos(theta)**9 + 4759394443514.65*cos(theta)**7 - 1074701971116.21*cos(theta)**5 + 92646721647.9492*cos(theta)**3 - 2058816036.62109*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl18_m_minus_6(theta, phi):
    return 6.74258724725256e-8*(1.0 - cos(theta)**2)**3*(462718904230.591*cos(theta)**12 - 872555647977.686*cos(theta)**10 + 594924305439.331*cos(theta)**8 - 179116995186.035*cos(theta)**6 + 23161680411.9873*cos(theta)**4 - 1029408018.31055*cos(theta)**2 + 6862720.12207031)*sin(6*phi)

#@torch.jit.script
def Yl18_m_minus_5(theta, phi):
    return 1.19097836376173e-6*(1.0 - cos(theta)**2)**2.5*(35593761863.8916*cos(theta)**13 - 79323240725.2441*cos(theta)**11 + 66102700604.3701*cos(theta)**9 - 25588142169.4336*cos(theta)**7 + 4632336082.39746*cos(theta)**5 - 343136006.103516*cos(theta)**3 + 6862720.12207031*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl18_m_minus_4(theta, phi):
    return 2.13713426594923e-5*(1.0 - cos(theta)**2)**2*(2542411561.70654*cos(theta)**14 - 6610270060.43701*cos(theta)**12 + 6610270060.43701*cos(theta)**10 - 3198517771.1792*cos(theta)**8 + 772056013.73291*cos(theta)**6 - 85784001.5258789*cos(theta)**4 + 3431360.06103516*cos(theta)**2 - 21312.7954101563)*sin(4*phi)

#@torch.jit.script
def Yl18_m_minus_3(theta, phi):
    return 0.000388229719023305*(1.0 - cos(theta)**2)**1.5*(169494104.11377*cos(theta)**15 - 508482312.341309*cos(theta)**13 + 600933641.85791*cos(theta)**11 - 355390863.464355*cos(theta)**9 + 110293716.247559*cos(theta)**7 - 17156800.3051758*cos(theta)**5 + 1143786.68701172*cos(theta)**3 - 21312.7954101563*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl18_m_minus_2(theta, phi):
    return 0.00711636829782292*(1.0 - cos(theta)**2)*(10593381.5071106*cos(theta)**16 - 36320165.1672363*cos(theta)**14 + 50077803.4881592*cos(theta)**12 - 35539086.3464355*cos(theta)**10 + 13786714.5309448*cos(theta)**8 - 2859466.7175293*cos(theta)**6 + 285946.67175293*cos(theta)**4 - 10656.3977050781*cos(theta)**2 + 63.4309387207031)*sin(2*phi)

#@torch.jit.script
def Yl18_m_minus_1(theta, phi):
    return 0.131219347792496*(1.0 - cos(theta)**2)**0.5*(623140.088653564*cos(theta)**17 - 2421344.34448242*cos(theta)**15 + 3852138.7298584*cos(theta)**13 - 3230826.03149414*cos(theta)**11 + 1531857.17010498*cos(theta)**9 - 408495.245361328*cos(theta)**7 + 57189.3343505859*cos(theta)**5 - 3552.13256835938*cos(theta)**3 + 63.4309387207031*cos(theta))*sin(phi)

#@torch.jit.script
def Yl18_m0(theta, phi):
    return 186620.345601326*cos(theta)**18 - 815797.51077151*cos(theta)**16 + 1483268.20140275*cos(theta)**14 - 1451369.96051236*cos(theta)**12 + 825779.460291517*cos(theta)**10 - 275259.820097172*cos(theta)**8 + 51381.8330848055*cos(theta)**6 - 4787.12730603778*cos(theta)**4 + 170.968832358492*cos(theta)**2 - 0.999817733090598

#@torch.jit.script
def Yl18_m1(theta, phi):
    return 0.131219347792496*(1.0 - cos(theta)**2)**0.5*(623140.088653564*cos(theta)**17 - 2421344.34448242*cos(theta)**15 + 3852138.7298584*cos(theta)**13 - 3230826.03149414*cos(theta)**11 + 1531857.17010498*cos(theta)**9 - 408495.245361328*cos(theta)**7 + 57189.3343505859*cos(theta)**5 - 3552.13256835938*cos(theta)**3 + 63.4309387207031*cos(theta))*cos(phi)

#@torch.jit.script
def Yl18_m2(theta, phi):
    return 0.00711636829782292*(1.0 - cos(theta)**2)*(10593381.5071106*cos(theta)**16 - 36320165.1672363*cos(theta)**14 + 50077803.4881592*cos(theta)**12 - 35539086.3464355*cos(theta)**10 + 13786714.5309448*cos(theta)**8 - 2859466.7175293*cos(theta)**6 + 285946.67175293*cos(theta)**4 - 10656.3977050781*cos(theta)**2 + 63.4309387207031)*cos(2*phi)

#@torch.jit.script
def Yl18_m3(theta, phi):
    return 0.000388229719023305*(1.0 - cos(theta)**2)**1.5*(169494104.11377*cos(theta)**15 - 508482312.341309*cos(theta)**13 + 600933641.85791*cos(theta)**11 - 355390863.464355*cos(theta)**9 + 110293716.247559*cos(theta)**7 - 17156800.3051758*cos(theta)**5 + 1143786.68701172*cos(theta)**3 - 21312.7954101563*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl18_m4(theta, phi):
    return 2.13713426594923e-5*(1.0 - cos(theta)**2)**2*(2542411561.70654*cos(theta)**14 - 6610270060.43701*cos(theta)**12 + 6610270060.43701*cos(theta)**10 - 3198517771.1792*cos(theta)**8 + 772056013.73291*cos(theta)**6 - 85784001.5258789*cos(theta)**4 + 3431360.06103516*cos(theta)**2 - 21312.7954101563)*cos(4*phi)

#@torch.jit.script
def Yl18_m5(theta, phi):
    return 1.19097836376173e-6*(1.0 - cos(theta)**2)**2.5*(35593761863.8916*cos(theta)**13 - 79323240725.2441*cos(theta)**11 + 66102700604.3701*cos(theta)**9 - 25588142169.4336*cos(theta)**7 + 4632336082.39746*cos(theta)**5 - 343136006.103516*cos(theta)**3 + 6862720.12207031*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl18_m6(theta, phi):
    return 6.74258724725256e-8*(1.0 - cos(theta)**2)**3*(462718904230.591*cos(theta)**12 - 872555647977.686*cos(theta)**10 + 594924305439.331*cos(theta)**8 - 179116995186.035*cos(theta)**6 + 23161680411.9873*cos(theta)**4 - 1029408018.31055*cos(theta)**2 + 6862720.12207031)*cos(6*phi)

#@torch.jit.script
def Yl18_m7(theta, phi):
    return 3.8928345622358e-9*(1.0 - cos(theta)**2)**3.5*(5552626850767.09*cos(theta)**11 - 8725556479776.86*cos(theta)**9 + 4759394443514.65*cos(theta)**7 - 1074701971116.21*cos(theta)**5 + 92646721647.9492*cos(theta)**3 - 2058816036.62109*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl18_m8(theta, phi):
    return 2.30188133218476e-10*(1.0 - cos(theta)**2)**4*(61078895358438.0*cos(theta)**10 - 78530008317991.7*cos(theta)**8 + 33315761104602.5*cos(theta)**6 - 5373509855581.05*cos(theta)**4 + 277940164943.848*cos(theta)**2 - 2058816036.62109)*cos(8*phi)

#@torch.jit.script
def Yl18_m9(theta, phi):
    return 1.40088036704182e-11*(1.0 - cos(theta)**2)**4.5*(610788953584380.0*cos(theta)**9 - 628240066543934.0*cos(theta)**7 + 199894566627615.0*cos(theta)**5 - 21494039422324.2*cos(theta)**3 + 555880329887.695*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl18_m10(theta, phi):
    return 8.82471682796557e-13*(1.0 - cos(theta)**2)**5*(5.49710058225942e+15*cos(theta)**8 - 4.39768046580754e+15*cos(theta)**6 + 999472833138076.0*cos(theta)**4 - 64482118266972.7*cos(theta)**2 + 555880329887.695)*cos(10*phi)

#@torch.jit.script
def Yl18_m11(theta, phi):
    return 5.79371043838662e-14*(1.0 - cos(theta)**2)**5.5*(4.39768046580754e+16*cos(theta)**7 - 2.63860827948452e+16*cos(theta)**5 + 3.9978913325523e+15*cos(theta)**3 - 128964236533945.0*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl18_m12(theta, phi):
    return 3.9980400343329e-15*(1.0 - cos(theta)**2)**6*(3.07837632606527e+17*cos(theta)**6 - 1.31930413974226e+17*cos(theta)**4 + 1.19936739976569e+16*cos(theta)**2 - 128964236533945.0)*cos(12*phi)

#@torch.jit.script
def Yl18_m13(theta, phi):
    return 2.93150518387396e-16*(1.0 - cos(theta)**2)**6.5*(1.84702579563916e+18*cos(theta)**5 - 5.27721655896904e+17*cos(theta)**3 + 2.39873479953138e+16*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl18_m14(theta, phi):
    return 2.31755833840811e-17*(1.0 - cos(theta)**2)**7*(9.23512897819582e+18*cos(theta)**4 - 1.58316496769071e+18*cos(theta)**2 + 2.39873479953138e+16)*cos(14*phi)

#@torch.jit.script
def Yl18_m15(theta, phi):
    return 2.01717561545333e-18*(1.0 - cos(theta)**2)**7.5*(3.69405159127833e+19*cos(theta)**3 - 3.16632993538143e+18*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl18_m16(theta, phi):
    return 1.99730147939357e-19*(1.0 - cos(theta)**2)**8*(1.1082154773835e+20*cos(theta)**2 - 3.16632993538143e+18)*cos(16*phi)

#@torch.jit.script
def Yl18_m17(theta, phi):
    return 5.29113461206997*(1.0 - cos(theta)**2)**8.5*cos(17*phi)*cos(theta)

#@torch.jit.script
def Yl18_m18(theta, phi):
    return 0.881855768678329*(1.0 - cos(theta)**2)**9*cos(18*phi)

#@torch.jit.script
def Yl19_m_minus_19(theta, phi):
    return 0.893383784349949*(1.0 - cos(theta)**2)**9.5*sin(19*phi)

#@torch.jit.script
def Yl19_m_minus_18(theta, phi):
    return 5.50718751027224*(1.0 - cos(theta)**2)**9*sin(18*phi)*cos(theta)

#@torch.jit.script
def Yl19_m_minus_17(theta, phi):
    return 5.77683273022057e-21*(1.0 - cos(theta)**2)**8.5*(4.10039726631895e+21*cos(theta)**2 - 1.1082154773835e+20)*sin(17*phi)

#@torch.jit.script
def Yl19_m_minus_16(theta, phi):
    return 6.00346067734132e-20*(1.0 - cos(theta)**2)**8*(1.36679908877298e+21*cos(theta)**3 - 1.1082154773835e+20*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl19_m_minus_15(theta, phi):
    return 7.1033904683705e-19*(1.0 - cos(theta)**2)**7.5*(3.41699772193245e+20*cos(theta)**4 - 5.54107738691749e+19*cos(theta)**2 + 7.91582483845356e+17)*sin(15*phi)

#@torch.jit.script
def Yl19_m_minus_14(theta, phi):
    return 9.26168804529891e-18*(1.0 - cos(theta)**2)**7*(6.83399544386491e+19*cos(theta)**5 - 1.84702579563916e+19*cos(theta)**3 + 7.91582483845356e+17*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl19_m_minus_13(theta, phi):
    return 1.30323502710715e-16*(1.0 - cos(theta)**2)**6.5*(1.13899924064415e+19*cos(theta)**6 - 4.61756448909791e+18*cos(theta)**4 + 3.95791241922678e+17*cos(theta)**2 - 3.9978913325523e+15)*sin(13*phi)

#@torch.jit.script
def Yl19_m_minus_12(theta, phi):
    return 1.9505035863512e-15*(1.0 - cos(theta)**2)**6*(1.62714177234879e+18*cos(theta)**7 - 9.23512897819582e+17*cos(theta)**5 + 1.31930413974226e+17*cos(theta)**3 - 3.9978913325523e+15*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl19_m_minus_11(theta, phi):
    return 3.07165611944352e-14*(1.0 - cos(theta)**2)**5.5*(2.03392721543598e+17*cos(theta)**8 - 1.53918816303264e+17*cos(theta)**6 + 3.29826034935565e+16*cos(theta)**4 - 1.99894566627615e+15*cos(theta)**2 + 16120529566743.2)*sin(11*phi)

#@torch.jit.script
def Yl19_m_minus_10(theta, phi):
    return 5.047246036554e-13*(1.0 - cos(theta)**2)**5*(2.25991912826221e+16*cos(theta)**9 - 2.19884023290377e+16*cos(theta)**7 + 6.5965206987113e+15*cos(theta)**5 - 666315222092051.0*cos(theta)**3 + 16120529566743.2*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl19_m_minus_9(theta, phi):
    return 8.59515028403688e-12*(1.0 - cos(theta)**2)**4.5*(2.25991912826221e+15*cos(theta)**10 - 2.74855029112971e+15*cos(theta)**8 + 1.09942011645188e+15*cos(theta)**6 - 166578805523013.0*cos(theta)**4 + 8060264783371.58*cos(theta)**2 - 55588032988.7695)*sin(9*phi)

#@torch.jit.script
def Yl19_m_minus_8(theta, phi):
    return 1.50844275293414e-10*(1.0 - cos(theta)**2)**4*(205447193478382.0*cos(theta)**11 - 305394476792190.0*cos(theta)**9 + 157060016635983.0*cos(theta)**7 - 33315761104602.5*cos(theta)**5 + 2686754927790.53*cos(theta)**3 - 55588032988.7695*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl19_m_minus_7(theta, phi):
    return 2.71519695528145e-9*(1.0 - cos(theta)**2)**3.5*(17120599456531.9*cos(theta)**12 - 30539447679219.0*cos(theta)**10 + 19632502079497.9*cos(theta)**8 - 5552626850767.09*cos(theta)**6 + 671688731947.632*cos(theta)**4 - 27794016494.3848*cos(theta)**2 + 171568003.051758)*sin(7*phi)

#@torch.jit.script
def Yl19_m_minus_6(theta, phi):
    return 4.99182886627511e-8*(1.0 - cos(theta)**2)**3*(1316969188963.99*cos(theta)**13 - 2776313425383.54*cos(theta)**11 + 2181389119944.21*cos(theta)**9 - 793232407252.441*cos(theta)**7 + 134337746389.526*cos(theta)**5 - 9264672164.79492*cos(theta)**3 + 171568003.051758*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl19_m_minus_5(theta, phi):
    return 9.33885667550482e-7*(1.0 - cos(theta)**2)**2.5*(94069227783.1421*cos(theta)**14 - 231359452115.295*cos(theta)**12 + 218138911994.421*cos(theta)**10 - 99154050906.5552*cos(theta)**8 + 22389624398.2544*cos(theta)**6 - 2316168041.19873*cos(theta)**4 + 85784001.5258789*cos(theta)**2 - 490194.294433594)*sin(5*phi)

#@torch.jit.script
def Yl19_m_minus_4(theta, phi):
    return 1.77192347018779e-5*(1.0 - cos(theta)**2)**2*(6271281852.20947*cos(theta)**15 - 17796880931.9458*cos(theta)**13 + 19830810181.311*cos(theta)**11 - 11017116767.395*cos(theta)**9 + 3198517771.1792*cos(theta)**7 - 463233608.239746*cos(theta)**5 + 28594667.175293*cos(theta)**3 - 490194.294433594*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl19_m_minus_3(theta, phi):
    return 0.000339913857408971*(1.0 - cos(theta)**2)**1.5*(391955115.763092*cos(theta)**16 - 1271205780.85327*cos(theta)**14 + 1652567515.10925*cos(theta)**12 - 1101711676.7395*cos(theta)**10 + 399814721.3974*cos(theta)**8 - 77205601.373291*cos(theta)**6 + 7148666.79382324*cos(theta)**4 - 245097.147216797*cos(theta)**2 + 1332.04971313477)*sin(3*phi)

#@torch.jit.script
def Yl19_m_minus_2(theta, phi):
    return 0.00657362114755131*(1.0 - cos(theta)**2)*(23056183.2801819*cos(theta)**17 - 84747052.0568848*cos(theta)**15 + 127120578.085327*cos(theta)**13 - 100155606.976318*cos(theta)**11 + 44423857.9330444*cos(theta)**9 - 11029371.6247559*cos(theta)**7 + 1429733.35876465*cos(theta)**5 - 81699.0490722656*cos(theta)**3 + 1332.04971313477*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl19_m_minus_1(theta, phi):
    return 0.127805802320551*(1.0 - cos(theta)**2)**0.5*(1280899.07112122*cos(theta)**18 - 5296690.7535553*cos(theta)**16 + 9080041.29180908*cos(theta)**14 - 8346300.58135986*cos(theta)**12 + 4442385.79330444*cos(theta)**10 - 1378671.45309448*cos(theta)**8 + 238288.893127441*cos(theta)**6 - 20424.7622680664*cos(theta)**4 + 666.024856567383*cos(theta)**2 - 3.52394104003906)*sin(phi)

#@torch.jit.script
def Yl19_m0(theta, phi):
    return 373111.430353337*cos(theta)**19 - 1724379.85379515*cos(theta)**17 + 3350223.71594487*cos(theta)**15 - 3553267.57751728*cos(theta)**13 + 2235119.92779313*cos(theta)**11 - 847804.110542221*cos(theta)**9 + 188400.913453827*cos(theta)**7 - 22608.1096144592*cos(theta)**5 + 1228.70160948148*cos(theta)**3 - 19.5032001504997*cos(theta)

#@torch.jit.script
def Yl19_m1(theta, phi):
    return 0.127805802320551*(1.0 - cos(theta)**2)**0.5*(1280899.07112122*cos(theta)**18 - 5296690.7535553*cos(theta)**16 + 9080041.29180908*cos(theta)**14 - 8346300.58135986*cos(theta)**12 + 4442385.79330444*cos(theta)**10 - 1378671.45309448*cos(theta)**8 + 238288.893127441*cos(theta)**6 - 20424.7622680664*cos(theta)**4 + 666.024856567383*cos(theta)**2 - 3.52394104003906)*cos(phi)

#@torch.jit.script
def Yl19_m2(theta, phi):
    return 0.00657362114755131*(1.0 - cos(theta)**2)*(23056183.2801819*cos(theta)**17 - 84747052.0568848*cos(theta)**15 + 127120578.085327*cos(theta)**13 - 100155606.976318*cos(theta)**11 + 44423857.9330444*cos(theta)**9 - 11029371.6247559*cos(theta)**7 + 1429733.35876465*cos(theta)**5 - 81699.0490722656*cos(theta)**3 + 1332.04971313477*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl19_m3(theta, phi):
    return 0.000339913857408971*(1.0 - cos(theta)**2)**1.5*(391955115.763092*cos(theta)**16 - 1271205780.85327*cos(theta)**14 + 1652567515.10925*cos(theta)**12 - 1101711676.7395*cos(theta)**10 + 399814721.3974*cos(theta)**8 - 77205601.373291*cos(theta)**6 + 7148666.79382324*cos(theta)**4 - 245097.147216797*cos(theta)**2 + 1332.04971313477)*cos(3*phi)

#@torch.jit.script
def Yl19_m4(theta, phi):
    return 1.77192347018779e-5*(1.0 - cos(theta)**2)**2*(6271281852.20947*cos(theta)**15 - 17796880931.9458*cos(theta)**13 + 19830810181.311*cos(theta)**11 - 11017116767.395*cos(theta)**9 + 3198517771.1792*cos(theta)**7 - 463233608.239746*cos(theta)**5 + 28594667.175293*cos(theta)**3 - 490194.294433594*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl19_m5(theta, phi):
    return 9.33885667550482e-7*(1.0 - cos(theta)**2)**2.5*(94069227783.1421*cos(theta)**14 - 231359452115.295*cos(theta)**12 + 218138911994.421*cos(theta)**10 - 99154050906.5552*cos(theta)**8 + 22389624398.2544*cos(theta)**6 - 2316168041.19873*cos(theta)**4 + 85784001.5258789*cos(theta)**2 - 490194.294433594)*cos(5*phi)

#@torch.jit.script
def Yl19_m6(theta, phi):
    return 4.99182886627511e-8*(1.0 - cos(theta)**2)**3*(1316969188963.99*cos(theta)**13 - 2776313425383.54*cos(theta)**11 + 2181389119944.21*cos(theta)**9 - 793232407252.441*cos(theta)**7 + 134337746389.526*cos(theta)**5 - 9264672164.79492*cos(theta)**3 + 171568003.051758*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl19_m7(theta, phi):
    return 2.71519695528145e-9*(1.0 - cos(theta)**2)**3.5*(17120599456531.9*cos(theta)**12 - 30539447679219.0*cos(theta)**10 + 19632502079497.9*cos(theta)**8 - 5552626850767.09*cos(theta)**6 + 671688731947.632*cos(theta)**4 - 27794016494.3848*cos(theta)**2 + 171568003.051758)*cos(7*phi)

#@torch.jit.script
def Yl19_m8(theta, phi):
    return 1.50844275293414e-10*(1.0 - cos(theta)**2)**4*(205447193478382.0*cos(theta)**11 - 305394476792190.0*cos(theta)**9 + 157060016635983.0*cos(theta)**7 - 33315761104602.5*cos(theta)**5 + 2686754927790.53*cos(theta)**3 - 55588032988.7695*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl19_m9(theta, phi):
    return 8.59515028403688e-12*(1.0 - cos(theta)**2)**4.5*(2.25991912826221e+15*cos(theta)**10 - 2.74855029112971e+15*cos(theta)**8 + 1.09942011645188e+15*cos(theta)**6 - 166578805523013.0*cos(theta)**4 + 8060264783371.58*cos(theta)**2 - 55588032988.7695)*cos(9*phi)

#@torch.jit.script
def Yl19_m10(theta, phi):
    return 5.047246036554e-13*(1.0 - cos(theta)**2)**5*(2.25991912826221e+16*cos(theta)**9 - 2.19884023290377e+16*cos(theta)**7 + 6.5965206987113e+15*cos(theta)**5 - 666315222092051.0*cos(theta)**3 + 16120529566743.2*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl19_m11(theta, phi):
    return 3.07165611944352e-14*(1.0 - cos(theta)**2)**5.5*(2.03392721543598e+17*cos(theta)**8 - 1.53918816303264e+17*cos(theta)**6 + 3.29826034935565e+16*cos(theta)**4 - 1.99894566627615e+15*cos(theta)**2 + 16120529566743.2)*cos(11*phi)

#@torch.jit.script
def Yl19_m12(theta, phi):
    return 1.9505035863512e-15*(1.0 - cos(theta)**2)**6*(1.62714177234879e+18*cos(theta)**7 - 9.23512897819582e+17*cos(theta)**5 + 1.31930413974226e+17*cos(theta)**3 - 3.9978913325523e+15*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl19_m13(theta, phi):
    return 1.30323502710715e-16*(1.0 - cos(theta)**2)**6.5*(1.13899924064415e+19*cos(theta)**6 - 4.61756448909791e+18*cos(theta)**4 + 3.95791241922678e+17*cos(theta)**2 - 3.9978913325523e+15)*cos(13*phi)

#@torch.jit.script
def Yl19_m14(theta, phi):
    return 9.26168804529891e-18*(1.0 - cos(theta)**2)**7*(6.83399544386491e+19*cos(theta)**5 - 1.84702579563916e+19*cos(theta)**3 + 7.91582483845356e+17*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl19_m15(theta, phi):
    return 7.1033904683705e-19*(1.0 - cos(theta)**2)**7.5*(3.41699772193245e+20*cos(theta)**4 - 5.54107738691749e+19*cos(theta)**2 + 7.91582483845356e+17)*cos(15*phi)

#@torch.jit.script
def Yl19_m16(theta, phi):
    return 6.00346067734132e-20*(1.0 - cos(theta)**2)**8*(1.36679908877298e+21*cos(theta)**3 - 1.1082154773835e+20*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl19_m17(theta, phi):
    return 5.77683273022057e-21*(1.0 - cos(theta)**2)**8.5*(4.10039726631895e+21*cos(theta)**2 - 1.1082154773835e+20)*cos(17*phi)

#@torch.jit.script
def Yl19_m18(theta, phi):
    return 5.50718751027224*(1.0 - cos(theta)**2)**9*cos(18*phi)*cos(theta)

#@torch.jit.script
def Yl19_m19(theta, phi):
    return 0.893383784349949*(1.0 - cos(theta)**2)**9.5*cos(19*phi)

#@torch.jit.script
def Yl20_m_minus_20(theta, phi):
    return 0.904482145093491*(1.0 - cos(theta)**2)**10*sin(20*phi)

#@torch.jit.script
def Yl20_m_minus_19(theta, phi):
    return 5.72044736290064*(1.0 - cos(theta)**2)**9.5*sin(19*phi)*cos(theta)

#@torch.jit.script
def Yl20_m_minus_18(theta, phi):
    return 1.57963503371958e-22*(1.0 - cos(theta)**2)**9*(1.59915493386439e+23*cos(theta)**2 - 4.10039726631895e+21)*sin(18*phi)

#@torch.jit.script
def Yl20_m_minus_17(theta, phi):
    return 1.68658868646741e-21*(1.0 - cos(theta)**2)**8.5*(5.33051644621463e+22*cos(theta)**3 - 4.10039726631895e+21*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl20_m_minus_16(theta, phi):
    return 2.05182369321377e-20*(1.0 - cos(theta)**2)**8*(1.33262911155366e+22*cos(theta)**4 - 2.05019863315947e+21*cos(theta)**2 + 2.77053869345875e+19)*sin(16*phi)

#@torch.jit.script
def Yl20_m_minus_15(theta, phi):
    return 2.7528103535224e-19*(1.0 - cos(theta)**2)**7.5*(2.66525822310731e+21*cos(theta)**5 - 6.83399544386491e+20*cos(theta)**3 + 2.77053869345875e+19*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl20_m_minus_14(theta, phi):
    return 3.9892011943704e-18*(1.0 - cos(theta)**2)**7*(4.44209703851219e+20*cos(theta)**6 - 1.70849886096623e+20*cos(theta)**4 + 1.38526934672937e+19*cos(theta)**2 - 1.31930413974226e+17)*sin(14*phi)

#@torch.jit.script
def Yl20_m_minus_13(theta, phi):
    return 6.15423986229134e-17*(1.0 - cos(theta)**2)**6.5*(6.34585291216027e+19*cos(theta)**7 - 3.41699772193245e+19*cos(theta)**5 + 4.61756448909791e+18*cos(theta)**3 - 1.31930413974226e+17*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl20_m_minus_12(theta, phi):
    return 9.99945619851927e-16*(1.0 - cos(theta)**2)**6*(7.93231614020034e+18*cos(theta)**8 - 5.69499620322076e+18*cos(theta)**6 + 1.15439112227448e+18*cos(theta)**4 - 6.5965206987113e+16*cos(theta)**2 + 499736416569038.0)*sin(12*phi)

#@torch.jit.script
def Yl20_m_minus_11(theta, phi):
    return 1.6969639886762e-14*(1.0 - cos(theta)**2)**5.5*(8.8136846002226e+17*cos(theta)**9 - 8.13570886174394e+17*cos(theta)**7 + 2.30878224454896e+17*cos(theta)**5 - 2.19884023290377e+16*cos(theta)**3 + 499736416569038.0*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl20_m_minus_10(theta, phi):
    return 2.98781341694522e-13*(1.0 - cos(theta)**2)**5*(8.8136846002226e+16*cos(theta)**10 - 1.01696360771799e+17*cos(theta)**8 + 3.84797040758159e+16*cos(theta)**6 - 5.49710058225942e+15*cos(theta)**4 + 249868208284519.0*cos(theta)**2 - 1612052956674.32)*sin(10*phi)

#@torch.jit.script
def Yl20_m_minus_9(theta, phi):
    return 5.42763260987486e-12*(1.0 - cos(theta)**2)**4.5*(8.01244054565691e+15*cos(theta)**11 - 1.1299595641311e+16*cos(theta)**9 + 5.49710058225942e+15*cos(theta)**7 - 1.09942011645188e+15*cos(theta)**5 + 83289402761506.3*cos(theta)**3 - 1612052956674.32*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl20_m_minus_8(theta, phi):
    return 1.01251173426417e-10*(1.0 - cos(theta)**2)**4*(667703378804743.0*cos(theta)**12 - 1.1299595641311e+15*cos(theta)**10 + 687137572782427.0*cos(theta)**8 - 183236686075314.0*cos(theta)**6 + 20822350690376.6*cos(theta)**4 - 806026478337.158*cos(theta)**2 + 4632336082.39746)*sin(8*phi)

#@torch.jit.script
def Yl20_m_minus_7(theta, phi):
    return 1.9317492704185e-9*(1.0 - cos(theta)**2)**3.5*(51361798369595.6*cos(theta)**13 - 102723596739191.0*cos(theta)**11 + 76348619198047.5*cos(theta)**9 - 26176669439330.6*cos(theta)**7 + 4164470138075.32*cos(theta)**5 - 268675492779.053*cos(theta)**3 + 4632336082.39746*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl20_m_minus_6(theta, phi):
    return 3.75574983477626e-8*(1.0 - cos(theta)**2)**3*(3668699883542.54*cos(theta)**14 - 8560299728265.93*cos(theta)**12 + 7634861919804.75*cos(theta)**10 - 3272083679916.32*cos(theta)**8 + 694078356345.886*cos(theta)**6 - 67168873194.7632*cos(theta)**4 + 2316168041.19873*cos(theta)**2 - 12254857.3608398)*sin(6*phi)

#@torch.jit.script
def Yl20_m_minus_5(theta, phi):
    return 7.417011635662e-7*(1.0 - cos(theta)**2)**2.5*(244579992236.169*cos(theta)**15 - 658484594481.995*cos(theta)**13 + 694078356345.886*cos(theta)**11 - 363564853324.036*cos(theta)**9 + 99154050906.5552*cos(theta)**7 - 13433774638.9526*cos(theta)**5 + 772056013.73291*cos(theta)**3 - 12254857.3608398*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl20_m_minus_4(theta, phi):
    return 1.4834023271324e-5*(1.0 - cos(theta)**2)**2*(15286249514.7606*cos(theta)**16 - 47034613891.571*cos(theta)**14 + 57839863028.8239*cos(theta)**12 - 36356485332.4036*cos(theta)**10 + 12394256363.3194*cos(theta)**8 - 2238962439.82544*cos(theta)**6 + 193014003.433228*cos(theta)**4 - 6127428.68041992*cos(theta)**2 + 30637.1434020996)*sin(4*phi)

#@torch.jit.script
def Yl20_m_minus_3(theta, phi):
    return 0.000299632582569029*(1.0 - cos(theta)**2)**1.5*(899191147.927094*cos(theta)**17 - 3135640926.10474*cos(theta)**15 + 4449220232.98645*cos(theta)**13 - 3305135030.21851*cos(theta)**11 + 1377139595.92438*cos(theta)**9 - 319851777.11792*cos(theta)**7 + 38602800.6866455*cos(theta)**5 - 2042476.22680664*cos(theta)**3 + 30637.1434020996*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl20_m_minus_2(theta, phi):
    return 0.00609662114603756*(1.0 - cos(theta)**2)*(49955063.7737274*cos(theta)**18 - 195977557.881546*cos(theta)**16 + 317801445.213318*cos(theta)**14 - 275427919.184875*cos(theta)**12 + 137713959.592438*cos(theta)**10 - 39981472.13974*cos(theta)**8 + 6433800.11444092*cos(theta)**6 - 510619.05670166*cos(theta)**4 + 15318.5717010498*cos(theta)**2 - 74.0027618408203)*sin(2*phi)

#@torch.jit.script
def Yl20_m_minus_1(theta, phi):
    return 0.12464571379913*(1.0 - cos(theta)**2)**0.5*(2629213.88282776*cos(theta)**19 - 11528091.6400909*cos(theta)**17 + 21186763.0142212*cos(theta)**15 - 21186763.0142212*cos(theta)**13 + 12519450.8720398*cos(theta)**11 - 4442385.79330444*cos(theta)**9 + 919114.302062988*cos(theta)**7 - 102123.811340332*cos(theta)**5 + 5106.1905670166*cos(theta)**3 - 74.0027618408203*cos(theta))*sin(phi)

#@torch.jit.script
def Yl20_m0(theta, phi):
    return 745989.629614649*cos(theta)**20 - 3634308.4519688*cos(theta)**18 + 7514178.28582739*cos(theta)**16 - 8587632.32665987*cos(theta)**14 + 5920261.67974279*cos(theta)**12 - 2520885.61847112*cos(theta)**10 + 651953.177190808*cos(theta)**8 - 96585.6558801197*cos(theta)**6 + 7243.92419100898*cos(theta)**4 - 209.968817130695*cos(theta)**2 + 0.999851510146167

#@torch.jit.script
def Yl20_m1(theta, phi):
    return 0.12464571379913*(1.0 - cos(theta)**2)**0.5*(2629213.88282776*cos(theta)**19 - 11528091.6400909*cos(theta)**17 + 21186763.0142212*cos(theta)**15 - 21186763.0142212*cos(theta)**13 + 12519450.8720398*cos(theta)**11 - 4442385.79330444*cos(theta)**9 + 919114.302062988*cos(theta)**7 - 102123.811340332*cos(theta)**5 + 5106.1905670166*cos(theta)**3 - 74.0027618408203*cos(theta))*cos(phi)

#@torch.jit.script
def Yl20_m2(theta, phi):
    return 0.00609662114603756*(1.0 - cos(theta)**2)*(49955063.7737274*cos(theta)**18 - 195977557.881546*cos(theta)**16 + 317801445.213318*cos(theta)**14 - 275427919.184875*cos(theta)**12 + 137713959.592438*cos(theta)**10 - 39981472.13974*cos(theta)**8 + 6433800.11444092*cos(theta)**6 - 510619.05670166*cos(theta)**4 + 15318.5717010498*cos(theta)**2 - 74.0027618408203)*cos(2*phi)

#@torch.jit.script
def Yl20_m3(theta, phi):
    return 0.000299632582569029*(1.0 - cos(theta)**2)**1.5*(899191147.927094*cos(theta)**17 - 3135640926.10474*cos(theta)**15 + 4449220232.98645*cos(theta)**13 - 3305135030.21851*cos(theta)**11 + 1377139595.92438*cos(theta)**9 - 319851777.11792*cos(theta)**7 + 38602800.6866455*cos(theta)**5 - 2042476.22680664*cos(theta)**3 + 30637.1434020996*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl20_m4(theta, phi):
    return 1.4834023271324e-5*(1.0 - cos(theta)**2)**2*(15286249514.7606*cos(theta)**16 - 47034613891.571*cos(theta)**14 + 57839863028.8239*cos(theta)**12 - 36356485332.4036*cos(theta)**10 + 12394256363.3194*cos(theta)**8 - 2238962439.82544*cos(theta)**6 + 193014003.433228*cos(theta)**4 - 6127428.68041992*cos(theta)**2 + 30637.1434020996)*cos(4*phi)

#@torch.jit.script
def Yl20_m5(theta, phi):
    return 7.417011635662e-7*(1.0 - cos(theta)**2)**2.5*(244579992236.169*cos(theta)**15 - 658484594481.995*cos(theta)**13 + 694078356345.886*cos(theta)**11 - 363564853324.036*cos(theta)**9 + 99154050906.5552*cos(theta)**7 - 13433774638.9526*cos(theta)**5 + 772056013.73291*cos(theta)**3 - 12254857.3608398*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl20_m6(theta, phi):
    return 3.75574983477626e-8*(1.0 - cos(theta)**2)**3*(3668699883542.54*cos(theta)**14 - 8560299728265.93*cos(theta)**12 + 7634861919804.75*cos(theta)**10 - 3272083679916.32*cos(theta)**8 + 694078356345.886*cos(theta)**6 - 67168873194.7632*cos(theta)**4 + 2316168041.19873*cos(theta)**2 - 12254857.3608398)*cos(6*phi)

#@torch.jit.script
def Yl20_m7(theta, phi):
    return 1.9317492704185e-9*(1.0 - cos(theta)**2)**3.5*(51361798369595.6*cos(theta)**13 - 102723596739191.0*cos(theta)**11 + 76348619198047.5*cos(theta)**9 - 26176669439330.6*cos(theta)**7 + 4164470138075.32*cos(theta)**5 - 268675492779.053*cos(theta)**3 + 4632336082.39746*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl20_m8(theta, phi):
    return 1.01251173426417e-10*(1.0 - cos(theta)**2)**4*(667703378804743.0*cos(theta)**12 - 1.1299595641311e+15*cos(theta)**10 + 687137572782427.0*cos(theta)**8 - 183236686075314.0*cos(theta)**6 + 20822350690376.6*cos(theta)**4 - 806026478337.158*cos(theta)**2 + 4632336082.39746)*cos(8*phi)

#@torch.jit.script
def Yl20_m9(theta, phi):
    return 5.42763260987486e-12*(1.0 - cos(theta)**2)**4.5*(8.01244054565691e+15*cos(theta)**11 - 1.1299595641311e+16*cos(theta)**9 + 5.49710058225942e+15*cos(theta)**7 - 1.09942011645188e+15*cos(theta)**5 + 83289402761506.3*cos(theta)**3 - 1612052956674.32*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl20_m10(theta, phi):
    return 2.98781341694522e-13*(1.0 - cos(theta)**2)**5*(8.8136846002226e+16*cos(theta)**10 - 1.01696360771799e+17*cos(theta)**8 + 3.84797040758159e+16*cos(theta)**6 - 5.49710058225942e+15*cos(theta)**4 + 249868208284519.0*cos(theta)**2 - 1612052956674.32)*cos(10*phi)

#@torch.jit.script
def Yl20_m11(theta, phi):
    return 1.6969639886762e-14*(1.0 - cos(theta)**2)**5.5*(8.8136846002226e+17*cos(theta)**9 - 8.13570886174394e+17*cos(theta)**7 + 2.30878224454896e+17*cos(theta)**5 - 2.19884023290377e+16*cos(theta)**3 + 499736416569038.0*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl20_m12(theta, phi):
    return 9.99945619851927e-16*(1.0 - cos(theta)**2)**6*(7.93231614020034e+18*cos(theta)**8 - 5.69499620322076e+18*cos(theta)**6 + 1.15439112227448e+18*cos(theta)**4 - 6.5965206987113e+16*cos(theta)**2 + 499736416569038.0)*cos(12*phi)

#@torch.jit.script
def Yl20_m13(theta, phi):
    return 6.15423986229134e-17*(1.0 - cos(theta)**2)**6.5*(6.34585291216027e+19*cos(theta)**7 - 3.41699772193245e+19*cos(theta)**5 + 4.61756448909791e+18*cos(theta)**3 - 1.31930413974226e+17*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl20_m14(theta, phi):
    return 3.9892011943704e-18*(1.0 - cos(theta)**2)**7*(4.44209703851219e+20*cos(theta)**6 - 1.70849886096623e+20*cos(theta)**4 + 1.38526934672937e+19*cos(theta)**2 - 1.31930413974226e+17)*cos(14*phi)

#@torch.jit.script
def Yl20_m15(theta, phi):
    return 2.7528103535224e-19*(1.0 - cos(theta)**2)**7.5*(2.66525822310731e+21*cos(theta)**5 - 6.83399544386491e+20*cos(theta)**3 + 2.77053869345875e+19*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl20_m16(theta, phi):
    return 2.05182369321377e-20*(1.0 - cos(theta)**2)**8*(1.33262911155366e+22*cos(theta)**4 - 2.05019863315947e+21*cos(theta)**2 + 2.77053869345875e+19)*cos(16*phi)

#@torch.jit.script
def Yl20_m17(theta, phi):
    return 1.68658868646741e-21*(1.0 - cos(theta)**2)**8.5*(5.33051644621463e+22*cos(theta)**3 - 4.10039726631895e+21*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl20_m18(theta, phi):
    return 1.57963503371958e-22*(1.0 - cos(theta)**2)**9*(1.59915493386439e+23*cos(theta)**2 - 4.10039726631895e+21)*cos(18*phi)

#@torch.jit.script
def Yl20_m19(theta, phi):
    return 5.72044736290064*(1.0 - cos(theta)**2)**9.5*cos(19*phi)*cos(theta)

#@torch.jit.script
def Yl20_m20(theta, phi):
    return 0.904482145093491*(1.0 - cos(theta)**2)**10*cos(20*phi)

#@torch.jit.script
def Yl21_m_minus_21(theta, phi):
    return 0.915186448400331*(1.0 - cos(theta)**2)**10.5*sin(21*phi)

#@torch.jit.script
def Yl21_m_minus_20(theta, phi):
    return 5.93108606277937*(1.0 - cos(theta)**2)**10*sin(20*phi)*cos(theta)

#@torch.jit.script
def Yl21_m_minus_19(theta, phi):
    return 4.09578128625229e-24*(1.0 - cos(theta)**2)**9.5*(6.55653522884399e+24*cos(theta)**2 - 1.59915493386439e+23)*sin(19*phi)

#@torch.jit.script
def Yl21_m_minus_18(theta, phi):
    return 4.48670360217581e-23*(1.0 - cos(theta)**2)**9*(2.185511742948e+24*cos(theta)**3 - 1.59915493386439e+23*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl21_m_minus_17(theta, phi):
    return 5.60389100299896e-22*(1.0 - cos(theta)**2)**8.5*(5.46377935737e+23*cos(theta)**4 - 7.99577466932194e+22*cos(theta)**2 + 1.02509931657974e+21)*sin(17*phi)

#@torch.jit.script
def Yl21_m_minus_16(theta, phi):
    return 7.72443067867375e-21*(1.0 - cos(theta)**2)**8*(1.092755871474e+23*cos(theta)**5 - 2.66525822310731e+22*cos(theta)**3 + 1.02509931657974e+21*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl21_m_minus_15(theta, phi):
    return 1.15091424992218e-19*(1.0 - cos(theta)**2)**7.5*(1.82125978579e+22*cos(theta)**6 - 6.66314555776829e+21*cos(theta)**4 + 5.12549658289868e+20*cos(theta)**2 - 4.61756448909791e+18)*sin(15*phi)

#@torch.jit.script
def Yl21_m_minus_14(theta, phi):
    return 1.82701973139271e-18*(1.0 - cos(theta)**2)**7*(2.60179969398571e+21*cos(theta)**7 - 1.33262911155366e+21*cos(theta)**5 + 1.70849886096623e+20*cos(theta)**3 - 4.61756448909791e+18*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl21_m_minus_13(theta, phi):
    return 3.05718875389061e-17*(1.0 - cos(theta)**2)**6.5*(3.25224961748214e+20*cos(theta)**8 - 2.2210485192561e+20*cos(theta)**6 + 4.27124715241557e+19*cos(theta)**4 - 2.30878224454896e+18*cos(theta)**2 + 1.64913017467783e+16)*sin(13*phi)

#@torch.jit.script
def Yl21_m_minus_12(theta, phi):
    return 5.34789616721945e-16*(1.0 - cos(theta)**2)**6*(3.61361068609127e+19*cos(theta)**9 - 3.17292645608014e+19*cos(theta)**7 + 8.54249430483114e+18*cos(theta)**5 - 7.69594081516319e+17*cos(theta)**3 + 1.64913017467783e+16*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl21_m_minus_11(theta, phi):
    return 9.71493583461516e-15*(1.0 - cos(theta)**2)**5.5*(3.61361068609127e+18*cos(theta)**10 - 3.96615807010017e+18*cos(theta)**8 + 1.42374905080519e+18*cos(theta)**6 - 1.9239852037908e+17*cos(theta)**4 + 8.24565087338913e+15*cos(theta)**2 - 49973641656903.8)*sin(11*phi)

#@torch.jit.script
def Yl21_m_minus_10(theta, phi):
    return 1.82268352577409e-13*(1.0 - cos(theta)**2)**5*(3.28510062371933e+17*cos(theta)**11 - 4.4068423001113e+17*cos(theta)**9 + 2.03392721543598e+17*cos(theta)**7 - 3.84797040758159e+16*cos(theta)**5 + 2.74855029112971e+15*cos(theta)**3 - 49973641656903.8*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl21_m_minus_9(theta, phi):
    return 3.51546467407613e-12*(1.0 - cos(theta)**2)**4.5*(2.73758385309944e+16*cos(theta)**12 - 4.4068423001113e+16*cos(theta)**10 + 2.54240901929498e+16*cos(theta)**8 - 6.41328401263599e+15*cos(theta)**6 + 687137572782427.0*cos(theta)**4 - 24986820828451.9*cos(theta)**2 + 134337746389.526)*sin(9*phi)

#@torch.jit.script
def Yl21_m_minus_8(theta, phi):
    return 6.94248646460625e-11*(1.0 - cos(theta)**2)**4*(2.10583373315342e+15*cos(theta)**13 - 4.00622027282846e+15*cos(theta)**11 + 2.82489891032776e+15*cos(theta)**9 - 916183430376570.0*cos(theta)**7 + 137427514556485.0*cos(theta)**5 - 8328940276150.63*cos(theta)**3 + 134337746389.526*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl21_m_minus_7(theta, phi):
    return 1.39887226130065e-9*(1.0 - cos(theta)**2)**3.5*(150416695225244.0*cos(theta)**14 - 333851689402371.0*cos(theta)**12 + 282489891032776.0*cos(theta)**10 - 114522928797071.0*cos(theta)**8 + 22904585759414.2*cos(theta)**6 - 2082235069037.66*cos(theta)**4 + 67168873194.7632*cos(theta)**2 - 330881148.742676)*sin(7*phi)

#@torch.jit.script
def Yl21_m_minus_6(theta, phi):
    return 2.86683503788286e-8*(1.0 - cos(theta)**2)**3*(10027779681682.9*cos(theta)**15 - 25680899184797.8*cos(theta)**13 + 25680899184797.8*cos(theta)**11 - 12724769866341.2*cos(theta)**9 + 3272083679916.32*cos(theta)**7 - 416447013807.532*cos(theta)**5 + 22389624398.2544*cos(theta)**3 - 330881148.742676*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl21_m_minus_5(theta, phi):
    return 5.95860473103812e-7*(1.0 - cos(theta)**2)**2.5*(626736230105.184*cos(theta)**16 - 1834349941771.27*cos(theta)**14 + 2140074932066.48*cos(theta)**12 - 1272476986634.12*cos(theta)**10 + 409010459989.54*cos(theta)**8 - 69407835634.5886*cos(theta)**6 + 5597406099.5636*cos(theta)**4 - 165440574.371338*cos(theta)**2 + 765928.58505249)*sin(5*phi)

#@torch.jit.script
def Yl21_m_minus_4(theta, phi):
    return 1.25272490558029e-5*(1.0 - cos(theta)**2)**2*(36866837065.0108*cos(theta)**17 - 122289996118.085*cos(theta)**15 + 164621148620.499*cos(theta)**13 - 115679726057.648*cos(theta)**11 + 45445606665.5045*cos(theta)**9 - 9915405090.65552*cos(theta)**7 + 1119481219.91272*cos(theta)**5 - 55146858.1237793*cos(theta)**3 + 765928.58505249*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl21_m_minus_3(theta, phi):
    return 0.00026574308270913*(1.0 - cos(theta)**2)**1.5*(2048157614.72282*cos(theta)**18 - 7643124757.38029*cos(theta)**16 + 11758653472.8928*cos(theta)**14 - 9639977171.47064*cos(theta)**12 + 4544560666.55045*cos(theta)**10 - 1239425636.33194*cos(theta)**8 + 186580203.318787*cos(theta)**6 - 13786714.5309448*cos(theta)**4 + 382964.292526245*cos(theta)**2 - 1702.06352233887)*sin(3*phi)

#@torch.jit.script
def Yl21_m_minus_2(theta, phi):
    return 0.00567471937804281*(1.0 - cos(theta)**2)*(107797769.195938*cos(theta)**19 - 449595573.963547*cos(theta)**17 + 783910231.526184*cos(theta)**15 - 741536705.497742*cos(theta)**13 + 413141878.777313*cos(theta)**11 - 137713959.592438*cos(theta)**9 + 26654314.7598267*cos(theta)**7 - 2757342.90618896*cos(theta)**5 + 127654.764175415*cos(theta)**3 - 1702.06352233887*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl21_m_minus_1(theta, phi):
    return 0.121709171425106*(1.0 - cos(theta)**2)**0.5*(5389888.45979691*cos(theta)**20 - 24977531.8868637*cos(theta)**18 + 48994389.4703865*cos(theta)**16 - 52966907.535553*cos(theta)**14 + 34428489.8981094*cos(theta)**12 - 13771395.9592438*cos(theta)**10 + 3331789.34497833*cos(theta)**8 - 459557.151031494*cos(theta)**6 + 31913.6910438538*cos(theta)**4 - 851.031761169434*cos(theta)**2 + 3.70013809204102)*sin(phi)

#@torch.jit.script
def Yl21_m0(theta, phi):
    return 1491556.30266255*cos(theta)**21 - 7639678.62339354*cos(theta)**19 + 16748526.2128243*cos(theta)**17 - 20520716.8012982*cos(theta)**15 + 15390537.6009737*cos(theta)**13 - 7275526.86591483*cos(theta)**11 + 2151365.47110385*cos(theta)**9 - 381522.940688367*cos(theta)**7 + 37092.5081224801*cos(theta)**5 - 1648.55591655467*cos(theta)**3 + 21.5029032594088*cos(theta)

#@torch.jit.script
def Yl21_m1(theta, phi):
    return 0.121709171425106*(1.0 - cos(theta)**2)**0.5*(5389888.45979691*cos(theta)**20 - 24977531.8868637*cos(theta)**18 + 48994389.4703865*cos(theta)**16 - 52966907.535553*cos(theta)**14 + 34428489.8981094*cos(theta)**12 - 13771395.9592438*cos(theta)**10 + 3331789.34497833*cos(theta)**8 - 459557.151031494*cos(theta)**6 + 31913.6910438538*cos(theta)**4 - 851.031761169434*cos(theta)**2 + 3.70013809204102)*cos(phi)

#@torch.jit.script
def Yl21_m2(theta, phi):
    return 0.00567471937804281*(1.0 - cos(theta)**2)*(107797769.195938*cos(theta)**19 - 449595573.963547*cos(theta)**17 + 783910231.526184*cos(theta)**15 - 741536705.497742*cos(theta)**13 + 413141878.777313*cos(theta)**11 - 137713959.592438*cos(theta)**9 + 26654314.7598267*cos(theta)**7 - 2757342.90618896*cos(theta)**5 + 127654.764175415*cos(theta)**3 - 1702.06352233887*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl21_m3(theta, phi):
    return 0.00026574308270913*(1.0 - cos(theta)**2)**1.5*(2048157614.72282*cos(theta)**18 - 7643124757.38029*cos(theta)**16 + 11758653472.8928*cos(theta)**14 - 9639977171.47064*cos(theta)**12 + 4544560666.55045*cos(theta)**10 - 1239425636.33194*cos(theta)**8 + 186580203.318787*cos(theta)**6 - 13786714.5309448*cos(theta)**4 + 382964.292526245*cos(theta)**2 - 1702.06352233887)*cos(3*phi)

#@torch.jit.script
def Yl21_m4(theta, phi):
    return 1.25272490558029e-5*(1.0 - cos(theta)**2)**2*(36866837065.0108*cos(theta)**17 - 122289996118.085*cos(theta)**15 + 164621148620.499*cos(theta)**13 - 115679726057.648*cos(theta)**11 + 45445606665.5045*cos(theta)**9 - 9915405090.65552*cos(theta)**7 + 1119481219.91272*cos(theta)**5 - 55146858.1237793*cos(theta)**3 + 765928.58505249*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl21_m5(theta, phi):
    return 5.95860473103812e-7*(1.0 - cos(theta)**2)**2.5*(626736230105.184*cos(theta)**16 - 1834349941771.27*cos(theta)**14 + 2140074932066.48*cos(theta)**12 - 1272476986634.12*cos(theta)**10 + 409010459989.54*cos(theta)**8 - 69407835634.5886*cos(theta)**6 + 5597406099.5636*cos(theta)**4 - 165440574.371338*cos(theta)**2 + 765928.58505249)*cos(5*phi)

#@torch.jit.script
def Yl21_m6(theta, phi):
    return 2.86683503788286e-8*(1.0 - cos(theta)**2)**3*(10027779681682.9*cos(theta)**15 - 25680899184797.8*cos(theta)**13 + 25680899184797.8*cos(theta)**11 - 12724769866341.2*cos(theta)**9 + 3272083679916.32*cos(theta)**7 - 416447013807.532*cos(theta)**5 + 22389624398.2544*cos(theta)**3 - 330881148.742676*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl21_m7(theta, phi):
    return 1.39887226130065e-9*(1.0 - cos(theta)**2)**3.5*(150416695225244.0*cos(theta)**14 - 333851689402371.0*cos(theta)**12 + 282489891032776.0*cos(theta)**10 - 114522928797071.0*cos(theta)**8 + 22904585759414.2*cos(theta)**6 - 2082235069037.66*cos(theta)**4 + 67168873194.7632*cos(theta)**2 - 330881148.742676)*cos(7*phi)

#@torch.jit.script
def Yl21_m8(theta, phi):
    return 6.94248646460625e-11*(1.0 - cos(theta)**2)**4*(2.10583373315342e+15*cos(theta)**13 - 4.00622027282846e+15*cos(theta)**11 + 2.82489891032776e+15*cos(theta)**9 - 916183430376570.0*cos(theta)**7 + 137427514556485.0*cos(theta)**5 - 8328940276150.63*cos(theta)**3 + 134337746389.526*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl21_m9(theta, phi):
    return 3.51546467407613e-12*(1.0 - cos(theta)**2)**4.5*(2.73758385309944e+16*cos(theta)**12 - 4.4068423001113e+16*cos(theta)**10 + 2.54240901929498e+16*cos(theta)**8 - 6.41328401263599e+15*cos(theta)**6 + 687137572782427.0*cos(theta)**4 - 24986820828451.9*cos(theta)**2 + 134337746389.526)*cos(9*phi)

#@torch.jit.script
def Yl21_m10(theta, phi):
    return 1.82268352577409e-13*(1.0 - cos(theta)**2)**5*(3.28510062371933e+17*cos(theta)**11 - 4.4068423001113e+17*cos(theta)**9 + 2.03392721543598e+17*cos(theta)**7 - 3.84797040758159e+16*cos(theta)**5 + 2.74855029112971e+15*cos(theta)**3 - 49973641656903.8*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl21_m11(theta, phi):
    return 9.71493583461516e-15*(1.0 - cos(theta)**2)**5.5*(3.61361068609127e+18*cos(theta)**10 - 3.96615807010017e+18*cos(theta)**8 + 1.42374905080519e+18*cos(theta)**6 - 1.9239852037908e+17*cos(theta)**4 + 8.24565087338913e+15*cos(theta)**2 - 49973641656903.8)*cos(11*phi)

#@torch.jit.script
def Yl21_m12(theta, phi):
    return 5.34789616721945e-16*(1.0 - cos(theta)**2)**6*(3.61361068609127e+19*cos(theta)**9 - 3.17292645608014e+19*cos(theta)**7 + 8.54249430483114e+18*cos(theta)**5 - 7.69594081516319e+17*cos(theta)**3 + 1.64913017467783e+16*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl21_m13(theta, phi):
    return 3.05718875389061e-17*(1.0 - cos(theta)**2)**6.5*(3.25224961748214e+20*cos(theta)**8 - 2.2210485192561e+20*cos(theta)**6 + 4.27124715241557e+19*cos(theta)**4 - 2.30878224454896e+18*cos(theta)**2 + 1.64913017467783e+16)*cos(13*phi)

#@torch.jit.script
def Yl21_m14(theta, phi):
    return 1.82701973139271e-18*(1.0 - cos(theta)**2)**7*(2.60179969398571e+21*cos(theta)**7 - 1.33262911155366e+21*cos(theta)**5 + 1.70849886096623e+20*cos(theta)**3 - 4.61756448909791e+18*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl21_m15(theta, phi):
    return 1.15091424992218e-19*(1.0 - cos(theta)**2)**7.5*(1.82125978579e+22*cos(theta)**6 - 6.66314555776829e+21*cos(theta)**4 + 5.12549658289868e+20*cos(theta)**2 - 4.61756448909791e+18)*cos(15*phi)

#@torch.jit.script
def Yl21_m16(theta, phi):
    return 7.72443067867375e-21*(1.0 - cos(theta)**2)**8*(1.092755871474e+23*cos(theta)**5 - 2.66525822310731e+22*cos(theta)**3 + 1.02509931657974e+21*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl21_m17(theta, phi):
    return 5.60389100299896e-22*(1.0 - cos(theta)**2)**8.5*(5.46377935737e+23*cos(theta)**4 - 7.99577466932194e+22*cos(theta)**2 + 1.02509931657974e+21)*cos(17*phi)

#@torch.jit.script
def Yl21_m18(theta, phi):
    return 4.48670360217581e-23*(1.0 - cos(theta)**2)**9*(2.185511742948e+24*cos(theta)**3 - 1.59915493386439e+23*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl21_m19(theta, phi):
    return 4.09578128625229e-24*(1.0 - cos(theta)**2)**9.5*(6.55653522884399e+24*cos(theta)**2 - 1.59915493386439e+23)*cos(19*phi)

#@torch.jit.script
def Yl21_m20(theta, phi):
    return 5.93108606277937*(1.0 - cos(theta)**2)**10*cos(20*phi)*cos(theta)

#@torch.jit.script
def Yl21_m21(theta, phi):
    return 0.915186448400331*(1.0 - cos(theta)**2)**10.5*cos(21*phi)

#@torch.jit.script
def Yl22_m_minus_22(theta, phi):
    return 0.925527866459589*(1.0 - cos(theta)**2)**11*sin(22*phi)

#@torch.jit.script
def Yl22_m_minus_21(theta, phi):
    return 6.13925733212923*(1.0 - cos(theta)**2)**10.5*sin(21*phi)*cos(theta)

#@torch.jit.script
def Yl22_m_minus_20(theta, phi):
    return 1.00969966670912e-25*(1.0 - cos(theta)**2)**10*(2.81931014840292e+26*cos(theta)**2 - 6.55653522884399e+24)*sin(20*phi)

#@torch.jit.script
def Yl22_m_minus_19(theta, phi):
    return 1.13338506490961e-24*(1.0 - cos(theta)**2)**9.5*(9.39770049467639e+25*cos(theta)**3 - 6.55653522884399e+24*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl22_m_minus_18(theta, phi):
    return 1.45144107589342e-23*(1.0 - cos(theta)**2)**9*(2.3494251236691e+25*cos(theta)**4 - 3.278267614422e+24*cos(theta)**2 + 3.99788733466097e+22)*sin(18*phi)

#@torch.jit.script
def Yl22_m_minus_17(theta, phi):
    return 2.05264765451388e-22*(1.0 - cos(theta)**2)**8.5*(4.6988502473382e+24*cos(theta)**5 - 1.092755871474e+24*cos(theta)**3 + 3.99788733466097e+22*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl22_m_minus_16(theta, phi):
    return 3.13994713346901e-21*(1.0 - cos(theta)**2)**8*(7.83141707889699e+23*cos(theta)**6 - 2.731889678685e+23*cos(theta)**4 + 1.99894366733049e+22*cos(theta)**2 - 1.70849886096623e+20)*sin(16*phi)

#@torch.jit.script
def Yl22_m_minus_15(theta, phi):
    return 5.12109879641152e-20*(1.0 - cos(theta)**2)**7.5*(1.11877386841386e+23*cos(theta)**7 - 5.46377935737e+22*cos(theta)**5 + 6.66314555776829e+21*cos(theta)**3 - 1.70849886096623e+20*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl22_m_minus_14(theta, phi):
    return 8.81067151427848e-19*(1.0 - cos(theta)**2)**7*(1.39846733551732e+22*cos(theta)**8 - 9.10629892894999e+21*cos(theta)**6 + 1.66578638944207e+21*cos(theta)**4 - 8.54249430483114e+19*cos(theta)**2 + 5.77195561137239e+17)*sin(14*phi)

#@torch.jit.script
def Yl22_m_minus_13(theta, phi):
    return 1.58592087257013e-17*(1.0 - cos(theta)**2)**6.5*(1.55385259501924e+21*cos(theta)**9 - 1.30089984699286e+21*cos(theta)**7 + 3.33157277888414e+20*cos(theta)**5 - 2.84749810161038e+19*cos(theta)**3 + 5.77195561137239e+17*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl22_m_minus_12(theta, phi):
    return 2.9669862738455e-16*(1.0 - cos(theta)**2)**6*(1.55385259501924e+20*cos(theta)**10 - 1.62612480874107e+20*cos(theta)**8 + 5.55262129814024e+19*cos(theta)**6 - 7.11874525402595e+18*cos(theta)**4 + 2.8859778056862e+17*cos(theta)**2 - 1.64913017467783e+15)*sin(12*phi)

#@torch.jit.script
def Yl22_m_minus_11(theta, phi):
    return 5.73787837392547e-15*(1.0 - cos(theta)**2)**5.5*(1.41259326819931e+19*cos(theta)**11 - 1.80680534304563e+19*cos(theta)**9 + 7.93231614020034e+18*cos(theta)**7 - 1.42374905080519e+18*cos(theta)**5 + 9.61992601895398e+16*cos(theta)**3 - 1.64913017467783e+15*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl22_m_minus_10(theta, phi):
    return 1.14182337954032e-13*(1.0 - cos(theta)**2)**5*(1.17716105683276e+18*cos(theta)**12 - 1.80680534304563e+18*cos(theta)**10 + 9.91539517525043e+17*cos(theta)**8 - 2.37291508467532e+17*cos(theta)**6 + 2.4049815047385e+16*cos(theta)**4 - 824565087338913.0*cos(theta)**2 + 4164470138075.32)*sin(10*phi)

#@torch.jit.script
def Yl22_m_minus_9(theta, phi):
    return 2.32887187734102e-12*(1.0 - cos(theta)**2)**4.5*(9.0550850525597e+16*cos(theta)**13 - 1.64255031185967e+17*cos(theta)**11 + 1.10171057502783e+17*cos(theta)**9 - 3.38987869239331e+16*cos(theta)**7 + 4.80996300947699e+15*cos(theta)**5 - 274855029112971.0*cos(theta)**3 + 4164470138075.32*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl22_m_minus_8(theta, phi):
    return 4.85166115051776e-11*(1.0 - cos(theta)**2)**4*(6.4679178946855e+15*cos(theta)**14 - 1.36879192654972e+16*cos(theta)**12 + 1.10171057502783e+16*cos(theta)**10 - 4.23734836549164e+15*cos(theta)**8 + 801660501579499.0*cos(theta)**6 - 68713757278242.7*cos(theta)**4 + 2082235069037.66*cos(theta)**2 - 9595553313.5376)*sin(8*phi)

#@torch.jit.script
def Yl22_m_minus_7(theta, phi):
    return 1.02919274986513e-9*(1.0 - cos(theta)**2)**3.5*(431194526312367.0*cos(theta)**15 - 1.05291686657671e+15*cos(theta)**13 + 1.00155506820711e+15*cos(theta)**11 - 470816485054626.0*cos(theta)**9 + 114522928797071.0*cos(theta)**7 - 13742751455648.5*cos(theta)**5 + 694078356345.886*cos(theta)**3 - 9595553313.5376*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl22_m_minus_6(theta, phi):
    return 2.21694903053267e-8*(1.0 - cos(theta)**2)**3*(26949657894522.9*cos(theta)**16 - 75208347612622.1*cos(theta)**14 + 83462922350592.8*cos(theta)**12 - 47081648505462.6*cos(theta)**10 + 14315366099633.9*cos(theta)**8 - 2290458575941.42*cos(theta)**6 + 173519589086.472*cos(theta)**4 - 4797776656.7688*cos(theta)**2 + 20680071.7964172)*sin(6*phi)

#@torch.jit.script
def Yl22_m_minus_5(theta, phi):
    return 4.83681174938034e-7*(1.0 - cos(theta)**2)**2.5*(1585273993795.47*cos(theta)**17 - 5013889840841.47*cos(theta)**15 + 6420224796199.45*cos(theta)**13 - 4280149864132.96*cos(theta)**11 + 1590596233292.66*cos(theta)**9 - 327208367991.632*cos(theta)**7 + 34703917817.2943*cos(theta)**5 - 1599258885.5896*cos(theta)**3 + 20680071.7964172*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl22_m_minus_4(theta, phi):
    return 1.06629486910923e-5*(1.0 - cos(theta)**2)**2*(88070777433.0814*cos(theta)**18 - 313368115052.592*cos(theta)**16 + 458587485442.818*cos(theta)**14 - 356679155344.414*cos(theta)**12 + 159059623329.266*cos(theta)**10 - 40901045998.954*cos(theta)**8 + 5783986302.88239*cos(theta)**6 - 399814721.3974*cos(theta)**4 + 10340035.8982086*cos(theta)**2 - 42551.5880584717)*sin(4*phi)

#@torch.jit.script
def Yl22_m_minus_3(theta, phi):
    return 0.000236995878752564*(1.0 - cos(theta)**2)**1.5*(4635304075.42534*cos(theta)**19 - 18433418532.5054*cos(theta)**17 + 30572499029.5212*cos(theta)**15 - 27436858103.4164*cos(theta)**13 + 14459965757.206*cos(theta)**11 - 4544560666.55045*cos(theta)**9 + 826283757.554626*cos(theta)**7 - 79962944.27948*cos(theta)**5 + 3446678.63273621*cos(theta)**3 - 42551.5880584717*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl22_m_minus_2(theta, phi):
    return 0.00529938895278031*(1.0 - cos(theta)**2)*(231765203.771267*cos(theta)**20 - 1024078807.36141*cos(theta)**18 + 1910781189.34507*cos(theta)**16 - 1959775578.81546*cos(theta)**14 + 1204997146.43383*cos(theta)**12 - 454456066.655045*cos(theta)**10 + 103285469.694328*cos(theta)**8 - 13327157.3799133*cos(theta)**6 + 861669.658184052*cos(theta)**4 - 21275.7940292358*cos(theta)**2 + 85.1031761169434)*sin(2*phi)

#@torch.jit.script
def Yl22_m_minus_1(theta, phi):
    return 0.118970986923352*(1.0 - cos(theta)**2)**0.5*(11036438.2748222*cos(theta)**21 - 53898884.5979691*cos(theta)**19 + 112398893.490887*cos(theta)**17 - 130651705.254364*cos(theta)**15 + 92692088.1872177*cos(theta)**13 - 41314187.8777313*cos(theta)**11 + 11476163.2993698*cos(theta)**9 - 1903879.6257019*cos(theta)**7 + 172333.93163681*cos(theta)**5 - 7091.93134307861*cos(theta)**3 + 85.1031761169434*cos(theta))*sin(phi)

#@torch.jit.script
def Yl22_m0(theta, phi):
    return 2982342.07383728*cos(theta)**22 - 16021419.0478235*cos(theta)**20 + 37122800.2327618*cos(theta)**18 - 48545200.3043808*cos(theta)**16 + 39360973.2197682*cos(theta)**14 - 20467706.0742795*cos(theta)**12 + 6822568.6914265*cos(theta)**10 - 1414818.3922313*cos(theta)**8 + 170753.943889985*cos(theta)**6 - 10540.3669067892*cos(theta)**4 + 252.96880576294*cos(theta)**2 - 0.999876702620317

#@torch.jit.script
def Yl22_m1(theta, phi):
    return 0.118970986923352*(1.0 - cos(theta)**2)**0.5*(11036438.2748222*cos(theta)**21 - 53898884.5979691*cos(theta)**19 + 112398893.490887*cos(theta)**17 - 130651705.254364*cos(theta)**15 + 92692088.1872177*cos(theta)**13 - 41314187.8777313*cos(theta)**11 + 11476163.2993698*cos(theta)**9 - 1903879.6257019*cos(theta)**7 + 172333.93163681*cos(theta)**5 - 7091.93134307861*cos(theta)**3 + 85.1031761169434*cos(theta))*cos(phi)

#@torch.jit.script
def Yl22_m2(theta, phi):
    return 0.00529938895278031*(1.0 - cos(theta)**2)*(231765203.771267*cos(theta)**20 - 1024078807.36141*cos(theta)**18 + 1910781189.34507*cos(theta)**16 - 1959775578.81546*cos(theta)**14 + 1204997146.43383*cos(theta)**12 - 454456066.655045*cos(theta)**10 + 103285469.694328*cos(theta)**8 - 13327157.3799133*cos(theta)**6 + 861669.658184052*cos(theta)**4 - 21275.7940292358*cos(theta)**2 + 85.1031761169434)*cos(2*phi)

#@torch.jit.script
def Yl22_m3(theta, phi):
    return 0.000236995878752564*(1.0 - cos(theta)**2)**1.5*(4635304075.42534*cos(theta)**19 - 18433418532.5054*cos(theta)**17 + 30572499029.5212*cos(theta)**15 - 27436858103.4164*cos(theta)**13 + 14459965757.206*cos(theta)**11 - 4544560666.55045*cos(theta)**9 + 826283757.554626*cos(theta)**7 - 79962944.27948*cos(theta)**5 + 3446678.63273621*cos(theta)**3 - 42551.5880584717*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl22_m4(theta, phi):
    return 1.06629486910923e-5*(1.0 - cos(theta)**2)**2*(88070777433.0814*cos(theta)**18 - 313368115052.592*cos(theta)**16 + 458587485442.818*cos(theta)**14 - 356679155344.414*cos(theta)**12 + 159059623329.266*cos(theta)**10 - 40901045998.954*cos(theta)**8 + 5783986302.88239*cos(theta)**6 - 399814721.3974*cos(theta)**4 + 10340035.8982086*cos(theta)**2 - 42551.5880584717)*cos(4*phi)

#@torch.jit.script
def Yl22_m5(theta, phi):
    return 4.83681174938034e-7*(1.0 - cos(theta)**2)**2.5*(1585273993795.47*cos(theta)**17 - 5013889840841.47*cos(theta)**15 + 6420224796199.45*cos(theta)**13 - 4280149864132.96*cos(theta)**11 + 1590596233292.66*cos(theta)**9 - 327208367991.632*cos(theta)**7 + 34703917817.2943*cos(theta)**5 - 1599258885.5896*cos(theta)**3 + 20680071.7964172*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl22_m6(theta, phi):
    return 2.21694903053267e-8*(1.0 - cos(theta)**2)**3*(26949657894522.9*cos(theta)**16 - 75208347612622.1*cos(theta)**14 + 83462922350592.8*cos(theta)**12 - 47081648505462.6*cos(theta)**10 + 14315366099633.9*cos(theta)**8 - 2290458575941.42*cos(theta)**6 + 173519589086.472*cos(theta)**4 - 4797776656.7688*cos(theta)**2 + 20680071.7964172)*cos(6*phi)

#@torch.jit.script
def Yl22_m7(theta, phi):
    return 1.02919274986513e-9*(1.0 - cos(theta)**2)**3.5*(431194526312367.0*cos(theta)**15 - 1.05291686657671e+15*cos(theta)**13 + 1.00155506820711e+15*cos(theta)**11 - 470816485054626.0*cos(theta)**9 + 114522928797071.0*cos(theta)**7 - 13742751455648.5*cos(theta)**5 + 694078356345.886*cos(theta)**3 - 9595553313.5376*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl22_m8(theta, phi):
    return 4.85166115051776e-11*(1.0 - cos(theta)**2)**4*(6.4679178946855e+15*cos(theta)**14 - 1.36879192654972e+16*cos(theta)**12 + 1.10171057502783e+16*cos(theta)**10 - 4.23734836549164e+15*cos(theta)**8 + 801660501579499.0*cos(theta)**6 - 68713757278242.7*cos(theta)**4 + 2082235069037.66*cos(theta)**2 - 9595553313.5376)*cos(8*phi)

#@torch.jit.script
def Yl22_m9(theta, phi):
    return 2.32887187734102e-12*(1.0 - cos(theta)**2)**4.5*(9.0550850525597e+16*cos(theta)**13 - 1.64255031185967e+17*cos(theta)**11 + 1.10171057502783e+17*cos(theta)**9 - 3.38987869239331e+16*cos(theta)**7 + 4.80996300947699e+15*cos(theta)**5 - 274855029112971.0*cos(theta)**3 + 4164470138075.32*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl22_m10(theta, phi):
    return 1.14182337954032e-13*(1.0 - cos(theta)**2)**5*(1.17716105683276e+18*cos(theta)**12 - 1.80680534304563e+18*cos(theta)**10 + 9.91539517525043e+17*cos(theta)**8 - 2.37291508467532e+17*cos(theta)**6 + 2.4049815047385e+16*cos(theta)**4 - 824565087338913.0*cos(theta)**2 + 4164470138075.32)*cos(10*phi)

#@torch.jit.script
def Yl22_m11(theta, phi):
    return 5.73787837392547e-15*(1.0 - cos(theta)**2)**5.5*(1.41259326819931e+19*cos(theta)**11 - 1.80680534304563e+19*cos(theta)**9 + 7.93231614020034e+18*cos(theta)**7 - 1.42374905080519e+18*cos(theta)**5 + 9.61992601895398e+16*cos(theta)**3 - 1.64913017467783e+15*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl22_m12(theta, phi):
    return 2.9669862738455e-16*(1.0 - cos(theta)**2)**6*(1.55385259501924e+20*cos(theta)**10 - 1.62612480874107e+20*cos(theta)**8 + 5.55262129814024e+19*cos(theta)**6 - 7.11874525402595e+18*cos(theta)**4 + 2.8859778056862e+17*cos(theta)**2 - 1.64913017467783e+15)*cos(12*phi)

#@torch.jit.script
def Yl22_m13(theta, phi):
    return 1.58592087257013e-17*(1.0 - cos(theta)**2)**6.5*(1.55385259501924e+21*cos(theta)**9 - 1.30089984699286e+21*cos(theta)**7 + 3.33157277888414e+20*cos(theta)**5 - 2.84749810161038e+19*cos(theta)**3 + 5.77195561137239e+17*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl22_m14(theta, phi):
    return 8.81067151427848e-19*(1.0 - cos(theta)**2)**7*(1.39846733551732e+22*cos(theta)**8 - 9.10629892894999e+21*cos(theta)**6 + 1.66578638944207e+21*cos(theta)**4 - 8.54249430483114e+19*cos(theta)**2 + 5.77195561137239e+17)*cos(14*phi)

#@torch.jit.script
def Yl22_m15(theta, phi):
    return 5.12109879641152e-20*(1.0 - cos(theta)**2)**7.5*(1.11877386841386e+23*cos(theta)**7 - 5.46377935737e+22*cos(theta)**5 + 6.66314555776829e+21*cos(theta)**3 - 1.70849886096623e+20*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl22_m16(theta, phi):
    return 3.13994713346901e-21*(1.0 - cos(theta)**2)**8*(7.83141707889699e+23*cos(theta)**6 - 2.731889678685e+23*cos(theta)**4 + 1.99894366733049e+22*cos(theta)**2 - 1.70849886096623e+20)*cos(16*phi)

#@torch.jit.script
def Yl22_m17(theta, phi):
    return 2.05264765451388e-22*(1.0 - cos(theta)**2)**8.5*(4.6988502473382e+24*cos(theta)**5 - 1.092755871474e+24*cos(theta)**3 + 3.99788733466097e+22*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl22_m18(theta, phi):
    return 1.45144107589342e-23*(1.0 - cos(theta)**2)**9*(2.3494251236691e+25*cos(theta)**4 - 3.278267614422e+24*cos(theta)**2 + 3.99788733466097e+22)*cos(18*phi)

#@torch.jit.script
def Yl22_m19(theta, phi):
    return 1.13338506490961e-24*(1.0 - cos(theta)**2)**9.5*(9.39770049467639e+25*cos(theta)**3 - 6.55653522884399e+24*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl22_m20(theta, phi):
    return 1.00969966670912e-25*(1.0 - cos(theta)**2)**10*(2.81931014840292e+26*cos(theta)**2 - 6.55653522884399e+24)*cos(20*phi)

#@torch.jit.script
def Yl22_m21(theta, phi):
    return 6.13925733212923*(1.0 - cos(theta)**2)**10.5*cos(21*phi)*cos(theta)

#@torch.jit.script
def Yl22_m22(theta, phi):
    return 0.925527866459589*(1.0 - cos(theta)**2)**11*cos(22*phi)

#@torch.jit.script
def Yl23_m_minus_23(theta, phi):
    return 0.935533863919911*(1.0 - cos(theta)**2)**11.5*sin(23*phi)

#@torch.jit.script
def Yl23_m_minus_22(theta, phi):
    return 6.34509937549305*(1.0 - cos(theta)**2)**11*sin(22*phi)*cos(theta)

#@torch.jit.script
def Yl23_m_minus_21(theta, phi):
    return 2.37232572869364e-27*(1.0 - cos(theta)**2)**10.5*(1.26868956678131e+28*cos(theta)**2 - 2.81931014840292e+26)*sin(21*phi)

#@torch.jit.script
def Yl23_m_minus_20(theta, phi):
    return 2.72559475329492e-26*(1.0 - cos(theta)**2)**10*(4.22896522260438e+27*cos(theta)**3 - 2.81931014840292e+26*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl23_m_minus_19(theta, phi):
    return 3.5745840073783e-25*(1.0 - cos(theta)**2)**9.5*(1.05724130565109e+27*cos(theta)**4 - 1.40965507420146e+26*cos(theta)**2 + 1.639133807211e+24)*sin(19*phi)

#@torch.jit.script
def Yl23_m_minus_18(theta, phi):
    return 5.18006435618226e-24*(1.0 - cos(theta)**2)**9*(2.11448261130219e+26*cos(theta)**5 - 4.6988502473382e+25*cos(theta)**3 + 1.639133807211e+24*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl23_m_minus_17(theta, phi):
    return 8.12461347795126e-23*(1.0 - cos(theta)**2)**8.5*(3.52413768550365e+25*cos(theta)**6 - 1.17471256183455e+25*cos(theta)**4 + 8.19566903605499e+23*cos(theta)**2 - 6.66314555776829e+21)*sin(17*phi)

#@torch.jit.script
def Yl23_m_minus_16(theta, phi):
    return 1.35950786560836e-21*(1.0 - cos(theta)**2)**8*(5.03448240786235e+24*cos(theta)**7 - 2.3494251236691e+24*cos(theta)**5 + 2.731889678685e+23*cos(theta)**3 - 6.66314555776829e+21*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl23_m_minus_15(theta, phi):
    return 2.40136967298897e-20*(1.0 - cos(theta)**2)**7.5*(6.29310300982794e+23*cos(theta)**8 - 3.9157085394485e+23*cos(theta)**6 + 6.82972419671249e+22*cos(theta)**4 - 3.33157277888414e+21*cos(theta)**2 + 2.13562357620778e+19)*sin(15*phi)

#@torch.jit.script
def Yl23_m_minus_14(theta, phi):
    return 4.44091105154346e-19*(1.0 - cos(theta)**2)**7*(6.9923366775866e+22*cos(theta)**9 - 5.59386934206928e+22*cos(theta)**7 + 1.3659448393425e+22*cos(theta)**5 - 1.11052425962805e+21*cos(theta)**3 + 2.13562357620778e+19*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl23_m_minus_13(theta, phi):
    return 8.54226296601593e-18*(1.0 - cos(theta)**2)**6.5*(6.9923366775866e+21*cos(theta)**10 - 6.9923366775866e+21*cos(theta)**8 + 2.2765747322375e+21*cos(theta)**6 - 2.77631064907012e+20*cos(theta)**4 + 1.06781178810389e+19*cos(theta)**2 - 5.77195561137239e+16)*sin(13*phi)

#@torch.jit.script
def Yl23_m_minus_12(theta, phi):
    return 1.6998888671294e-16*(1.0 - cos(theta)**2)**6*(6.35666970689691e+20*cos(theta)**11 - 7.76926297509622e+20*cos(theta)**9 + 3.25224961748214e+20*cos(theta)**7 - 5.55262129814024e+19*cos(theta)**5 + 3.55937262701297e+18*cos(theta)**3 - 5.77195561137239e+16*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl23_m_minus_11(theta, phi):
    return 3.48373550581555e-15*(1.0 - cos(theta)**2)**5.5*(5.29722475574742e+19*cos(theta)**12 - 7.76926297509622e+19*cos(theta)**10 + 4.06531202185268e+19*cos(theta)**8 - 9.25436883023373e+18*cos(theta)**6 + 8.89843156753243e+17*cos(theta)**4 - 2.88597780568619e+16*cos(theta)**2 + 137427514556485.0)*sin(11*phi)

#@torch.jit.script
def Yl23_m_minus_10(theta, phi):
    return 7.32413447372461e-14*(1.0 - cos(theta)**2)**5*(4.07478827365187e+18*cos(theta)**13 - 7.06296634099657e+18*cos(theta)**11 + 4.51701335761408e+18*cos(theta)**9 - 1.32205269003339e+18*cos(theta)**7 + 1.77968631350649e+17*cos(theta)**5 - 9.61992601895398e+15*cos(theta)**3 + 137427514556485.0*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl23_m_minus_9(theta, phi):
    return 1.57426303248889e-12*(1.0 - cos(theta)**2)**4.5*(2.91056305260848e+17*cos(theta)**14 - 5.88580528416381e+17*cos(theta)**12 + 4.51701335761408e+17*cos(theta)**10 - 1.65256586254174e+17*cos(theta)**8 + 2.96614385584414e+16*cos(theta)**6 - 2.4049815047385e+15*cos(theta)**4 + 68713757278242.7*cos(theta)**2 - 297462152719.666)*sin(9*phi)

#@torch.jit.script
def Yl23_m_minus_8(theta, phi):
    return 3.4490374973626e-11*(1.0 - cos(theta)**2)**4*(1.94037536840565e+16*cos(theta)**15 - 4.52754252627985e+16*cos(theta)**13 + 4.10637577964917e+16*cos(theta)**11 - 1.83618429171304e+16*cos(theta)**9 + 4.23734836549164e+15*cos(theta)**7 - 480996300947699.0*cos(theta)**5 + 22904585759414.2*cos(theta)**3 - 297462152719.666*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl23_m_minus_7(theta, phi):
    return 7.68137122555198e-10*(1.0 - cos(theta)**2)**3.5*(1.21273460525353e+15*cos(theta)**16 - 3.23395894734275e+15*cos(theta)**14 + 3.42197981637431e+15*cos(theta)**12 - 1.83618429171304e+15*cos(theta)**10 + 529668545686454.0*cos(theta)**8 - 80166050157949.9*cos(theta)**6 + 5726146439853.56*cos(theta)**4 - 148731076359.833*cos(theta)**2 + 599722082.0961)*sin(7*phi)

#@torch.jit.script
def Yl23_m_minus_6(theta, phi):
    return 1.73469785817059e-8*(1.0 - cos(theta)**2)**3*(71337329720796.0*cos(theta)**17 - 215597263156183.0*cos(theta)**15 + 263229216644177.0*cos(theta)**13 - 166925844701186.0*cos(theta)**11 + 58852060631828.3*cos(theta)**9 - 11452292879707.1*cos(theta)**7 + 1145229287970.71*cos(theta)**5 - 49577025453.2776*cos(theta)**3 + 599722082.0961*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl23_m_minus_5(theta, phi):
    return 3.96331958851659e-7*(1.0 - cos(theta)**2)**2.5*(3963184984488.66*cos(theta)**18 - 13474828947261.5*cos(theta)**16 + 18802086903155.5*cos(theta)**14 - 13910487058432.1*cos(theta)**12 + 5885206063182.83*cos(theta)**10 - 1431536609963.39*cos(theta)**8 + 190871547995.119*cos(theta)**6 - 12394256363.3194*cos(theta)**4 + 299861041.04805*cos(theta)**2 - 1148892.87757874)*sin(5*phi)

#@torch.jit.script
def Yl23_m_minus_4(theta, phi):
    return 9.1414462474505e-6*(1.0 - cos(theta)**2)**2*(208588683394.14*cos(theta)**19 - 792636996897.733*cos(theta)**17 + 1253472460210.37*cos(theta)**15 - 1070037466033.24*cos(theta)**13 + 535018733016.621*cos(theta)**11 - 159059623329.266*cos(theta)**9 + 27267363999.3027*cos(theta)**7 - 2478851272.66388*cos(theta)**5 + 99953680.34935*cos(theta)**3 - 1148892.87757874*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl23_m_minus_3(theta, phi):
    return 0.000212428014459756*(1.0 - cos(theta)**2)**1.5*(10429434169.707*cos(theta)**20 - 44035388716.5407*cos(theta)**18 + 78342028763.148*cos(theta)**16 - 76431247573.8029*cos(theta)**14 + 44584894418.0517*cos(theta)**12 - 15905962332.9266*cos(theta)**10 + 3408420499.91283*cos(theta)**8 - 413141878.777313*cos(theta)**6 + 24988420.0873375*cos(theta)**4 - 574446.438789368*cos(theta)**2 + 2127.57940292358)*sin(3*phi)

#@torch.jit.script
def Yl23_m_minus_2(theta, phi):
    return 0.00496372955394567*(1.0 - cos(theta)**2)*(496639722.367001*cos(theta)**21 - 2317652037.71267*cos(theta)**19 + 4608354633.12635*cos(theta)**17 - 5095416504.9202*cos(theta)**15 + 3429607262.92706*cos(theta)**13 - 1445996575.7206*cos(theta)**11 + 378713388.879204*cos(theta)**9 - 59020268.396759*cos(theta)**7 + 4997684.0174675*cos(theta)**5 - 191482.146263123*cos(theta)**3 + 2127.57940292358*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl23_m_minus_1(theta, phi):
    return 0.116409776636641*(1.0 - cos(theta)**2)**0.5*(22574532.8348637*cos(theta)**22 - 115882601.885633*cos(theta)**20 + 256019701.840353*cos(theta)**18 - 318463531.557512*cos(theta)**16 + 244971947.351933*cos(theta)**14 - 120499714.643383*cos(theta)**12 + 37871338.8879204*cos(theta)**10 - 7377533.54959488*cos(theta)**8 + 832947.336244583*cos(theta)**6 - 47870.5365657806*cos(theta)**4 + 1063.78970146179*cos(theta)**2 - 3.86832618713379)*sin(phi)

#@torch.jit.script
def Yl23_m0(theta, phi):
    return 5963274.55669477*cos(theta)**23 - 33526854.7298617*cos(theta)**21 + 81867901.084546*cos(theta)**19 - 113816350.288271*cos(theta)**17 + 99224510.5077237*cos(theta)**15 - 56316614.0719513*cos(theta)**13 + 20917599.5124391*cos(theta)**11 - 4980380.83629501*cos(theta)**9 + 722958.508494437*cos(theta)**7 - 58169.0753961042*cos(theta)**5 + 2154.41019985571*cos(theta)**3 - 23.5026567256986*cos(theta)

#@torch.jit.script
def Yl23_m1(theta, phi):
    return 0.116409776636641*(1.0 - cos(theta)**2)**0.5*(22574532.8348637*cos(theta)**22 - 115882601.885633*cos(theta)**20 + 256019701.840353*cos(theta)**18 - 318463531.557512*cos(theta)**16 + 244971947.351933*cos(theta)**14 - 120499714.643383*cos(theta)**12 + 37871338.8879204*cos(theta)**10 - 7377533.54959488*cos(theta)**8 + 832947.336244583*cos(theta)**6 - 47870.5365657806*cos(theta)**4 + 1063.78970146179*cos(theta)**2 - 3.86832618713379)*cos(phi)

#@torch.jit.script
def Yl23_m2(theta, phi):
    return 0.00496372955394567*(1.0 - cos(theta)**2)*(496639722.367001*cos(theta)**21 - 2317652037.71267*cos(theta)**19 + 4608354633.12635*cos(theta)**17 - 5095416504.9202*cos(theta)**15 + 3429607262.92706*cos(theta)**13 - 1445996575.7206*cos(theta)**11 + 378713388.879204*cos(theta)**9 - 59020268.396759*cos(theta)**7 + 4997684.0174675*cos(theta)**5 - 191482.146263123*cos(theta)**3 + 2127.57940292358*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl23_m3(theta, phi):
    return 0.000212428014459756*(1.0 - cos(theta)**2)**1.5*(10429434169.707*cos(theta)**20 - 44035388716.5407*cos(theta)**18 + 78342028763.148*cos(theta)**16 - 76431247573.8029*cos(theta)**14 + 44584894418.0517*cos(theta)**12 - 15905962332.9266*cos(theta)**10 + 3408420499.91283*cos(theta)**8 - 413141878.777313*cos(theta)**6 + 24988420.0873375*cos(theta)**4 - 574446.438789368*cos(theta)**2 + 2127.57940292358)*cos(3*phi)

#@torch.jit.script
def Yl23_m4(theta, phi):
    return 9.1414462474505e-6*(1.0 - cos(theta)**2)**2*(208588683394.14*cos(theta)**19 - 792636996897.733*cos(theta)**17 + 1253472460210.37*cos(theta)**15 - 1070037466033.24*cos(theta)**13 + 535018733016.621*cos(theta)**11 - 159059623329.266*cos(theta)**9 + 27267363999.3027*cos(theta)**7 - 2478851272.66388*cos(theta)**5 + 99953680.34935*cos(theta)**3 - 1148892.87757874*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl23_m5(theta, phi):
    return 3.96331958851659e-7*(1.0 - cos(theta)**2)**2.5*(3963184984488.66*cos(theta)**18 - 13474828947261.5*cos(theta)**16 + 18802086903155.5*cos(theta)**14 - 13910487058432.1*cos(theta)**12 + 5885206063182.83*cos(theta)**10 - 1431536609963.39*cos(theta)**8 + 190871547995.119*cos(theta)**6 - 12394256363.3194*cos(theta)**4 + 299861041.04805*cos(theta)**2 - 1148892.87757874)*cos(5*phi)

#@torch.jit.script
def Yl23_m6(theta, phi):
    return 1.73469785817059e-8*(1.0 - cos(theta)**2)**3*(71337329720796.0*cos(theta)**17 - 215597263156183.0*cos(theta)**15 + 263229216644177.0*cos(theta)**13 - 166925844701186.0*cos(theta)**11 + 58852060631828.3*cos(theta)**9 - 11452292879707.1*cos(theta)**7 + 1145229287970.71*cos(theta)**5 - 49577025453.2776*cos(theta)**3 + 599722082.0961*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl23_m7(theta, phi):
    return 7.68137122555198e-10*(1.0 - cos(theta)**2)**3.5*(1.21273460525353e+15*cos(theta)**16 - 3.23395894734275e+15*cos(theta)**14 + 3.42197981637431e+15*cos(theta)**12 - 1.83618429171304e+15*cos(theta)**10 + 529668545686454.0*cos(theta)**8 - 80166050157949.9*cos(theta)**6 + 5726146439853.56*cos(theta)**4 - 148731076359.833*cos(theta)**2 + 599722082.0961)*cos(7*phi)

#@torch.jit.script
def Yl23_m8(theta, phi):
    return 3.4490374973626e-11*(1.0 - cos(theta)**2)**4*(1.94037536840565e+16*cos(theta)**15 - 4.52754252627985e+16*cos(theta)**13 + 4.10637577964917e+16*cos(theta)**11 - 1.83618429171304e+16*cos(theta)**9 + 4.23734836549164e+15*cos(theta)**7 - 480996300947699.0*cos(theta)**5 + 22904585759414.2*cos(theta)**3 - 297462152719.666*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl23_m9(theta, phi):
    return 1.57426303248889e-12*(1.0 - cos(theta)**2)**4.5*(2.91056305260848e+17*cos(theta)**14 - 5.88580528416381e+17*cos(theta)**12 + 4.51701335761408e+17*cos(theta)**10 - 1.65256586254174e+17*cos(theta)**8 + 2.96614385584414e+16*cos(theta)**6 - 2.4049815047385e+15*cos(theta)**4 + 68713757278242.7*cos(theta)**2 - 297462152719.666)*cos(9*phi)

#@torch.jit.script
def Yl23_m10(theta, phi):
    return 7.32413447372461e-14*(1.0 - cos(theta)**2)**5*(4.07478827365187e+18*cos(theta)**13 - 7.06296634099657e+18*cos(theta)**11 + 4.51701335761408e+18*cos(theta)**9 - 1.32205269003339e+18*cos(theta)**7 + 1.77968631350649e+17*cos(theta)**5 - 9.61992601895398e+15*cos(theta)**3 + 137427514556485.0*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl23_m11(theta, phi):
    return 3.48373550581555e-15*(1.0 - cos(theta)**2)**5.5*(5.29722475574742e+19*cos(theta)**12 - 7.76926297509622e+19*cos(theta)**10 + 4.06531202185268e+19*cos(theta)**8 - 9.25436883023373e+18*cos(theta)**6 + 8.89843156753243e+17*cos(theta)**4 - 2.88597780568619e+16*cos(theta)**2 + 137427514556485.0)*cos(11*phi)

#@torch.jit.script
def Yl23_m12(theta, phi):
    return 1.6998888671294e-16*(1.0 - cos(theta)**2)**6*(6.35666970689691e+20*cos(theta)**11 - 7.76926297509622e+20*cos(theta)**9 + 3.25224961748214e+20*cos(theta)**7 - 5.55262129814024e+19*cos(theta)**5 + 3.55937262701297e+18*cos(theta)**3 - 5.77195561137239e+16*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl23_m13(theta, phi):
    return 8.54226296601593e-18*(1.0 - cos(theta)**2)**6.5*(6.9923366775866e+21*cos(theta)**10 - 6.9923366775866e+21*cos(theta)**8 + 2.2765747322375e+21*cos(theta)**6 - 2.77631064907012e+20*cos(theta)**4 + 1.06781178810389e+19*cos(theta)**2 - 5.77195561137239e+16)*cos(13*phi)

#@torch.jit.script
def Yl23_m14(theta, phi):
    return 4.44091105154346e-19*(1.0 - cos(theta)**2)**7*(6.9923366775866e+22*cos(theta)**9 - 5.59386934206928e+22*cos(theta)**7 + 1.3659448393425e+22*cos(theta)**5 - 1.11052425962805e+21*cos(theta)**3 + 2.13562357620778e+19*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl23_m15(theta, phi):
    return 2.40136967298897e-20*(1.0 - cos(theta)**2)**7.5*(6.29310300982794e+23*cos(theta)**8 - 3.9157085394485e+23*cos(theta)**6 + 6.82972419671249e+22*cos(theta)**4 - 3.33157277888414e+21*cos(theta)**2 + 2.13562357620778e+19)*cos(15*phi)

#@torch.jit.script
def Yl23_m16(theta, phi):
    return 1.35950786560836e-21*(1.0 - cos(theta)**2)**8*(5.03448240786235e+24*cos(theta)**7 - 2.3494251236691e+24*cos(theta)**5 + 2.731889678685e+23*cos(theta)**3 - 6.66314555776829e+21*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl23_m17(theta, phi):
    return 8.12461347795126e-23*(1.0 - cos(theta)**2)**8.5*(3.52413768550365e+25*cos(theta)**6 - 1.17471256183455e+25*cos(theta)**4 + 8.19566903605499e+23*cos(theta)**2 - 6.66314555776829e+21)*cos(17*phi)

#@torch.jit.script
def Yl23_m18(theta, phi):
    return 5.18006435618226e-24*(1.0 - cos(theta)**2)**9*(2.11448261130219e+26*cos(theta)**5 - 4.6988502473382e+25*cos(theta)**3 + 1.639133807211e+24*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl23_m19(theta, phi):
    return 3.5745840073783e-25*(1.0 - cos(theta)**2)**9.5*(1.05724130565109e+27*cos(theta)**4 - 1.40965507420146e+26*cos(theta)**2 + 1.639133807211e+24)*cos(19*phi)

#@torch.jit.script
def Yl23_m20(theta, phi):
    return 2.72559475329492e-26*(1.0 - cos(theta)**2)**10*(4.22896522260438e+27*cos(theta)**3 - 2.81931014840292e+26*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl23_m21(theta, phi):
    return 2.37232572869364e-27*(1.0 - cos(theta)**2)**10.5*(1.26868956678131e+28*cos(theta)**2 - 2.81931014840292e+26)*cos(21*phi)

#@torch.jit.script
def Yl23_m22(theta, phi):
    return 6.34509937549305*(1.0 - cos(theta)**2)**11*cos(22*phi)*cos(theta)

#@torch.jit.script
def Yl23_m23(theta, phi):
    return 0.935533863919911*(1.0 - cos(theta)**2)**11.5*cos(23*phi)

#@torch.jit.script
def Yl24_m_minus_24(theta, phi):
    return 0.9452287742978*(1.0 - cos(theta)**2)**12*sin(24*phi)

#@torch.jit.script
def Yl24_m_minus_23(theta, phi):
    return 6.54873704743938*(1.0 - cos(theta)**2)**11.5*sin(23*phi)*cos(theta)

#@torch.jit.script
def Yl24_m_minus_22(theta, phi):
    return 5.3240025801011e-29*(1.0 - cos(theta)**2)**11*(5.96284096387217e+29*cos(theta)**2 - 1.26868956678131e+28)*sin(22*phi)

#@torch.jit.script
def Yl24_m_minus_21(theta, phi):
    return 6.25428691320073e-28*(1.0 - cos(theta)**2)**10.5*(1.98761365462406e+29*cos(theta)**3 - 1.26868956678131e+28*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl24_m_minus_20(theta, phi):
    return 8.39100641322249e-27*(1.0 - cos(theta)**2)**10*(4.96903413656014e+28*cos(theta)**4 - 6.34344783390656e+27*cos(theta)**2 + 7.04827537100729e+25)*sin(20*phi)

#@torch.jit.script
def Yl24_m_minus_19(theta, phi):
    return 1.24458738133901e-25*(1.0 - cos(theta)**2)**9.5*(9.93806827312028e+27*cos(theta)**5 - 2.11448261130219e+27*cos(theta)**3 + 7.04827537100729e+25*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl24_m_minus_18(theta, phi):
    return 1.99910334761708e-24*(1.0 - cos(theta)**2)**9*(1.65634471218671e+27*cos(theta)**6 - 5.28620652825547e+26*cos(theta)**4 + 3.52413768550365e+25*cos(theta)**2 - 2.731889678685e+23)*sin(18*phi)

#@torch.jit.script
def Yl24_m_minus_17(theta, phi):
    return 3.42774820132609e-23*(1.0 - cos(theta)**2)**8.5*(2.36620673169531e+26*cos(theta)**7 - 1.05724130565109e+26*cos(theta)**5 + 1.17471256183455e+25*cos(theta)**3 - 2.731889678685e+23*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl24_m_minus_16(theta, phi):
    return 6.2079160239131e-22*(1.0 - cos(theta)**2)**8*(2.95775841461913e+25*cos(theta)**8 - 1.76206884275182e+25*cos(theta)**6 + 2.93678140458637e+24*cos(theta)**4 - 1.3659448393425e+23*cos(theta)**2 + 8.32893194721036e+20)*sin(16*phi)

#@torch.jit.script
def Yl24_m_minus_15(theta, phi):
    return 1.1778692495173e-20*(1.0 - cos(theta)**2)**7.5*(3.2863982384657e+24*cos(theta)**9 - 2.51724120393118e+24*cos(theta)**7 + 5.87356280917274e+23*cos(theta)**5 - 4.553149464475e+22*cos(theta)**3 + 8.32893194721036e+20*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl24_m_minus_14(theta, phi):
    return 2.32610538861376e-19*(1.0 - cos(theta)**2)**7*(3.2863982384657e+23*cos(theta)**10 - 3.14655150491397e+23*cos(theta)**8 + 9.78927134862124e+22*cos(theta)**6 - 1.13828736611875e+22*cos(theta)**4 + 4.16446597360518e+20*cos(theta)**2 - 2.13562357620778e+18)*sin(14*phi)

#@torch.jit.script
def Yl24_m_minus_13(theta, phi):
    return 4.75573370217054e-18*(1.0 - cos(theta)**2)**6.5*(2.98763476224155e+22*cos(theta)**11 - 3.4961683387933e+22*cos(theta)**9 + 1.39846733551732e+22*cos(theta)**7 - 2.2765747322375e+21*cos(theta)**5 + 1.38815532453506e+20*cos(theta)**3 - 2.13562357620778e+18*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl24_m_minus_12(theta, phi):
    return 1.00209527253683e-16*(1.0 - cos(theta)**2)**6*(2.48969563520129e+21*cos(theta)**12 - 3.4961683387933e+21*cos(theta)**10 + 1.74808416939665e+21*cos(theta)**8 - 3.79429122039583e+20*cos(theta)**6 + 3.47038831133765e+19*cos(theta)**4 - 1.06781178810389e+18*cos(theta)**2 + 4.80996300947699e+15)*sin(12*phi)

#@torch.jit.script
def Yl24_m_minus_11(theta, phi):
    return 2.16786353281895e-15*(1.0 - cos(theta)**2)**5.5*(1.91515048861638e+20*cos(theta)**13 - 3.17833485344846e+20*cos(theta)**11 + 1.94231574377406e+20*cos(theta)**9 - 5.4204160291369e+19*cos(theta)**7 + 6.9407766226753e+18*cos(theta)**5 - 3.55937262701297e+17*cos(theta)**3 + 4.80996300947699e+15*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl24_m_minus_10(theta, phi):
    return 4.79877049408895e-14*(1.0 - cos(theta)**2)**5*(1.36796463472598e+19*cos(theta)**14 - 2.64861237787371e+19*cos(theta)**12 + 1.94231574377406e+19*cos(theta)**10 - 6.77552003642113e+18*cos(theta)**8 + 1.15679610377922e+18*cos(theta)**6 - 8.89843156753244e+16*cos(theta)**4 + 2.4049815047385e+15*cos(theta)**2 - 9816251039748.96)*sin(10*phi)

#@torch.jit.script
def Yl24_m_minus_9(theta, phi):
    return 1.08371495837322e-12*(1.0 - cos(theta)**2)**4.5*(9.11976423150656e+17*cos(theta)**15 - 2.03739413682593e+18*cos(theta)**13 + 1.76574158524914e+18*cos(theta)**11 - 7.52835559602347e+17*cos(theta)**9 + 1.65256586254174e+17*cos(theta)**7 - 1.77968631350649e+16*cos(theta)**5 + 801660501579499.0*cos(theta)**3 - 9816251039748.96*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl24_m_minus_8(theta, phi):
    return 2.49018738774613e-11*(1.0 - cos(theta)**2)**4*(5.6998526446916e+16*cos(theta)**16 - 1.45528152630424e+17*cos(theta)**14 + 1.47145132104095e+17*cos(theta)**12 - 7.52835559602347e+16*cos(theta)**10 + 2.06570732817717e+16*cos(theta)**8 - 2.96614385584415e+15*cos(theta)**6 + 200415125394875.0*cos(theta)**4 - 4908125519874.48*cos(theta)**2 + 18591384544.9791)*sin(8*phi)

#@torch.jit.script
def Yl24_m_minus_7(theta, phi):
    return 5.80806514683927e-10*(1.0 - cos(theta)**2)**3.5*(3.35285449687741e+15*cos(theta)**17 - 9.70187684202825e+15*cos(theta)**15 + 1.13188563156996e+16*cos(theta)**13 - 6.84395963274861e+15*cos(theta)**11 + 2.2952303646413e+15*cos(theta)**9 - 423734836549164.0*cos(theta)**7 + 40083025078974.9*cos(theta)**5 - 1636041839958.16*cos(theta)**3 + 18591384544.9791*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl24_m_minus_6(theta, phi):
    return 1.37198252096958e-8*(1.0 - cos(theta)**2)**3*(186269694270967.0*cos(theta)**18 - 606367302626766.0*cos(theta)**16 + 808489736835688.0*cos(theta)**14 - 570329969395718.0*cos(theta)**12 + 229523036464130.0*cos(theta)**10 - 52966854568645.4*cos(theta)**8 + 6680504179829.16*cos(theta)**6 - 409010459989.54*cos(theta)**4 + 9295692272.48955*cos(theta)**2 - 33317893.4497833)*sin(6*phi)

#@torch.jit.script
def Yl24_m_minus_5(theta, phi):
    return 3.27556337379121e-7*(1.0 - cos(theta)**2)**2.5*(9803668119524.59*cos(theta)**19 - 35668664860398.0*cos(theta)**17 + 53899315789045.8*cos(theta)**15 - 43871536107362.9*cos(theta)**13 + 20865730587648.2*cos(theta)**11 - 5885206063182.83*cos(theta)**9 + 954357739975.594*cos(theta)**7 - 81802091997.908*cos(theta)**5 + 3098564090.82985*cos(theta)**3 - 33317893.4497833*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl24_m_minus_4(theta, phi):
    return 7.88860123286696e-6*(1.0 - cos(theta)**2)**2*(490183405976.23*cos(theta)**20 - 1981592492244.33*cos(theta)**18 + 3368707236815.36*cos(theta)**16 - 3133681150525.92*cos(theta)**14 + 1738810882304.02*cos(theta)**12 - 588520606318.283*cos(theta)**10 + 119294717496.949*cos(theta)**8 - 13633681999.6513*cos(theta)**6 + 774641022.707462*cos(theta)**4 - 16658946.7248917*cos(theta)**2 + 57444.6438789368)*sin(4*phi)

#@torch.jit.script
def Yl24_m_minus_3(theta, phi):
    return 0.000191288413903665*(1.0 - cos(theta)**2)**1.5*(23342066951.249*cos(theta)**21 - 104294341697.07*cos(theta)**19 + 198159249224.433*cos(theta)**17 - 208912076701.728*cos(theta)**15 + 133754683254.155*cos(theta)**13 - 53501873301.6621*cos(theta)**11 + 13254968610.7721*cos(theta)**9 - 1947668857.09305*cos(theta)**7 + 154928204.541492*cos(theta)**5 - 5552982.24163055*cos(theta)**3 + 57444.6438789368*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl24_m_minus_2(theta, phi):
    return 0.00466210326274582*(1.0 - cos(theta)**2)*(1061003043.23859*cos(theta)**22 - 5214717084.85351*cos(theta)**20 + 11008847179.1352*cos(theta)**18 - 13057004793.858*cos(theta)**16 + 9553905946.72537*cos(theta)**14 - 4458489441.80517*cos(theta)**12 + 1325496861.07721*cos(theta)**10 - 243458607.136631*cos(theta)**8 + 25821367.4235821*cos(theta)**6 - 1388245.56040764*cos(theta)**4 + 28722.3219394684*cos(theta)**2 - 96.7081546783447)*sin(2*phi)

#@torch.jit.script
def Yl24_m_minus_1(theta, phi):
    return 0.114007252777348*(1.0 - cos(theta)**2)**0.5*(46130567.0973301*cos(theta)**23 - 248319861.1835*cos(theta)**21 + 579413009.428167*cos(theta)**19 - 768059105.521059*cos(theta)**17 + 636927063.115025*cos(theta)**15 - 342960726.292706*cos(theta)**13 + 120499714.643383*cos(theta)**11 - 27050956.3485146*cos(theta)**9 + 3688766.77479744*cos(theta)**7 - 277649.112081528*cos(theta)**5 + 9574.10731315613*cos(theta)**3 - 96.7081546783447*cos(theta))*sin(phi)

#@torch.jit.script
def Yl24_m0(theta, phi):
    return 11923960.6056839*cos(theta)**24 - 70021555.8972075*cos(theta)**22 + 179721993.469499*cos(theta)**20 - 264706812.086859*cos(theta)**18 + 246952086.885911*cos(theta)**16 - 151970515.006715*cos(theta)**14 + 62294220.115365*cos(theta)**12 - 16781300.1127106*cos(theta)**10 + 2860448.88284839*cos(theta)**8 - 287070.138780484*cos(theta)**6 + 14848.455454163*cos(theta)**4 - 299.968797053797*cos(theta)**2 + 0.999895990179324

#@torch.jit.script
def Yl24_m1(theta, phi):
    return 0.114007252777348*(1.0 - cos(theta)**2)**0.5*(46130567.0973301*cos(theta)**23 - 248319861.1835*cos(theta)**21 + 579413009.428167*cos(theta)**19 - 768059105.521059*cos(theta)**17 + 636927063.115025*cos(theta)**15 - 342960726.292706*cos(theta)**13 + 120499714.643383*cos(theta)**11 - 27050956.3485146*cos(theta)**9 + 3688766.77479744*cos(theta)**7 - 277649.112081528*cos(theta)**5 + 9574.10731315613*cos(theta)**3 - 96.7081546783447*cos(theta))*cos(phi)

#@torch.jit.script
def Yl24_m2(theta, phi):
    return 0.00466210326274582*(1.0 - cos(theta)**2)*(1061003043.23859*cos(theta)**22 - 5214717084.85351*cos(theta)**20 + 11008847179.1352*cos(theta)**18 - 13057004793.858*cos(theta)**16 + 9553905946.72537*cos(theta)**14 - 4458489441.80517*cos(theta)**12 + 1325496861.07721*cos(theta)**10 - 243458607.136631*cos(theta)**8 + 25821367.4235821*cos(theta)**6 - 1388245.56040764*cos(theta)**4 + 28722.3219394684*cos(theta)**2 - 96.7081546783447)*cos(2*phi)

#@torch.jit.script
def Yl24_m3(theta, phi):
    return 0.000191288413903665*(1.0 - cos(theta)**2)**1.5*(23342066951.249*cos(theta)**21 - 104294341697.07*cos(theta)**19 + 198159249224.433*cos(theta)**17 - 208912076701.728*cos(theta)**15 + 133754683254.155*cos(theta)**13 - 53501873301.6621*cos(theta)**11 + 13254968610.7721*cos(theta)**9 - 1947668857.09305*cos(theta)**7 + 154928204.541492*cos(theta)**5 - 5552982.24163055*cos(theta)**3 + 57444.6438789368*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl24_m4(theta, phi):
    return 7.88860123286696e-6*(1.0 - cos(theta)**2)**2*(490183405976.23*cos(theta)**20 - 1981592492244.33*cos(theta)**18 + 3368707236815.36*cos(theta)**16 - 3133681150525.92*cos(theta)**14 + 1738810882304.02*cos(theta)**12 - 588520606318.283*cos(theta)**10 + 119294717496.949*cos(theta)**8 - 13633681999.6513*cos(theta)**6 + 774641022.707462*cos(theta)**4 - 16658946.7248917*cos(theta)**2 + 57444.6438789368)*cos(4*phi)

#@torch.jit.script
def Yl24_m5(theta, phi):
    return 3.27556337379121e-7*(1.0 - cos(theta)**2)**2.5*(9803668119524.59*cos(theta)**19 - 35668664860398.0*cos(theta)**17 + 53899315789045.8*cos(theta)**15 - 43871536107362.9*cos(theta)**13 + 20865730587648.2*cos(theta)**11 - 5885206063182.83*cos(theta)**9 + 954357739975.594*cos(theta)**7 - 81802091997.908*cos(theta)**5 + 3098564090.82985*cos(theta)**3 - 33317893.4497833*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl24_m6(theta, phi):
    return 1.37198252096958e-8*(1.0 - cos(theta)**2)**3*(186269694270967.0*cos(theta)**18 - 606367302626766.0*cos(theta)**16 + 808489736835688.0*cos(theta)**14 - 570329969395718.0*cos(theta)**12 + 229523036464130.0*cos(theta)**10 - 52966854568645.4*cos(theta)**8 + 6680504179829.16*cos(theta)**6 - 409010459989.54*cos(theta)**4 + 9295692272.48955*cos(theta)**2 - 33317893.4497833)*cos(6*phi)

#@torch.jit.script
def Yl24_m7(theta, phi):
    return 5.80806514683927e-10*(1.0 - cos(theta)**2)**3.5*(3.35285449687741e+15*cos(theta)**17 - 9.70187684202825e+15*cos(theta)**15 + 1.13188563156996e+16*cos(theta)**13 - 6.84395963274861e+15*cos(theta)**11 + 2.2952303646413e+15*cos(theta)**9 - 423734836549164.0*cos(theta)**7 + 40083025078974.9*cos(theta)**5 - 1636041839958.16*cos(theta)**3 + 18591384544.9791*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl24_m8(theta, phi):
    return 2.49018738774613e-11*(1.0 - cos(theta)**2)**4*(5.6998526446916e+16*cos(theta)**16 - 1.45528152630424e+17*cos(theta)**14 + 1.47145132104095e+17*cos(theta)**12 - 7.52835559602347e+16*cos(theta)**10 + 2.06570732817717e+16*cos(theta)**8 - 2.96614385584415e+15*cos(theta)**6 + 200415125394875.0*cos(theta)**4 - 4908125519874.48*cos(theta)**2 + 18591384544.9791)*cos(8*phi)

#@torch.jit.script
def Yl24_m9(theta, phi):
    return 1.08371495837322e-12*(1.0 - cos(theta)**2)**4.5*(9.11976423150656e+17*cos(theta)**15 - 2.03739413682593e+18*cos(theta)**13 + 1.76574158524914e+18*cos(theta)**11 - 7.52835559602347e+17*cos(theta)**9 + 1.65256586254174e+17*cos(theta)**7 - 1.77968631350649e+16*cos(theta)**5 + 801660501579499.0*cos(theta)**3 - 9816251039748.96*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl24_m10(theta, phi):
    return 4.79877049408895e-14*(1.0 - cos(theta)**2)**5*(1.36796463472598e+19*cos(theta)**14 - 2.64861237787371e+19*cos(theta)**12 + 1.94231574377406e+19*cos(theta)**10 - 6.77552003642113e+18*cos(theta)**8 + 1.15679610377922e+18*cos(theta)**6 - 8.89843156753244e+16*cos(theta)**4 + 2.4049815047385e+15*cos(theta)**2 - 9816251039748.96)*cos(10*phi)

#@torch.jit.script
def Yl24_m11(theta, phi):
    return 2.16786353281895e-15*(1.0 - cos(theta)**2)**5.5*(1.91515048861638e+20*cos(theta)**13 - 3.17833485344846e+20*cos(theta)**11 + 1.94231574377406e+20*cos(theta)**9 - 5.4204160291369e+19*cos(theta)**7 + 6.9407766226753e+18*cos(theta)**5 - 3.55937262701297e+17*cos(theta)**3 + 4.80996300947699e+15*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl24_m12(theta, phi):
    return 1.00209527253683e-16*(1.0 - cos(theta)**2)**6*(2.48969563520129e+21*cos(theta)**12 - 3.4961683387933e+21*cos(theta)**10 + 1.74808416939665e+21*cos(theta)**8 - 3.79429122039583e+20*cos(theta)**6 + 3.47038831133765e+19*cos(theta)**4 - 1.06781178810389e+18*cos(theta)**2 + 4.80996300947699e+15)*cos(12*phi)

#@torch.jit.script
def Yl24_m13(theta, phi):
    return 4.75573370217054e-18*(1.0 - cos(theta)**2)**6.5*(2.98763476224155e+22*cos(theta)**11 - 3.4961683387933e+22*cos(theta)**9 + 1.39846733551732e+22*cos(theta)**7 - 2.2765747322375e+21*cos(theta)**5 + 1.38815532453506e+20*cos(theta)**3 - 2.13562357620778e+18*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl24_m14(theta, phi):
    return 2.32610538861376e-19*(1.0 - cos(theta)**2)**7*(3.2863982384657e+23*cos(theta)**10 - 3.14655150491397e+23*cos(theta)**8 + 9.78927134862124e+22*cos(theta)**6 - 1.13828736611875e+22*cos(theta)**4 + 4.16446597360518e+20*cos(theta)**2 - 2.13562357620778e+18)*cos(14*phi)

#@torch.jit.script
def Yl24_m15(theta, phi):
    return 1.1778692495173e-20*(1.0 - cos(theta)**2)**7.5*(3.2863982384657e+24*cos(theta)**9 - 2.51724120393118e+24*cos(theta)**7 + 5.87356280917274e+23*cos(theta)**5 - 4.553149464475e+22*cos(theta)**3 + 8.32893194721036e+20*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl24_m16(theta, phi):
    return 6.2079160239131e-22*(1.0 - cos(theta)**2)**8*(2.95775841461913e+25*cos(theta)**8 - 1.76206884275182e+25*cos(theta)**6 + 2.93678140458637e+24*cos(theta)**4 - 1.3659448393425e+23*cos(theta)**2 + 8.32893194721036e+20)*cos(16*phi)

#@torch.jit.script
def Yl24_m17(theta, phi):
    return 3.42774820132609e-23*(1.0 - cos(theta)**2)**8.5*(2.36620673169531e+26*cos(theta)**7 - 1.05724130565109e+26*cos(theta)**5 + 1.17471256183455e+25*cos(theta)**3 - 2.731889678685e+23*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl24_m18(theta, phi):
    return 1.99910334761708e-24*(1.0 - cos(theta)**2)**9*(1.65634471218671e+27*cos(theta)**6 - 5.28620652825547e+26*cos(theta)**4 + 3.52413768550365e+25*cos(theta)**2 - 2.731889678685e+23)*cos(18*phi)

#@torch.jit.script
def Yl24_m19(theta, phi):
    return 1.24458738133901e-25*(1.0 - cos(theta)**2)**9.5*(9.93806827312028e+27*cos(theta)**5 - 2.11448261130219e+27*cos(theta)**3 + 7.04827537100729e+25*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl24_m20(theta, phi):
    return 8.39100641322249e-27*(1.0 - cos(theta)**2)**10*(4.96903413656014e+28*cos(theta)**4 - 6.34344783390656e+27*cos(theta)**2 + 7.04827537100729e+25)*cos(20*phi)

#@torch.jit.script
def Yl24_m21(theta, phi):
    return 6.25428691320073e-28*(1.0 - cos(theta)**2)**10.5*(1.98761365462406e+29*cos(theta)**3 - 1.26868956678131e+28*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl24_m22(theta, phi):
    return 5.3240025801011e-29*(1.0 - cos(theta)**2)**11*(5.96284096387217e+29*cos(theta)**2 - 1.26868956678131e+28)*cos(22*phi)

#@torch.jit.script
def Yl24_m23(theta, phi):
    return 6.54873704743938*(1.0 - cos(theta)**2)**11.5*cos(23*phi)*cos(theta)

#@torch.jit.script
def Yl24_m24(theta, phi):
    return 0.9452287742978*(1.0 - cos(theta)**2)**12*cos(24*phi)

#@torch.jit.script
def Yl25_m_minus_25(theta, phi):
    return 0.954634267390256*(1.0 - cos(theta)**2)**12.5*sin(25*phi)

#@torch.jit.script
def Yl25_m_minus_24(theta, phi):
    return 6.75028364024702*(1.0 - cos(theta)**2)**12*sin(24*phi)*cos(theta)

#@torch.jit.script
def Yl25_m_minus_23(theta, phi):
    return 1.14355157834306e-30*(1.0 - cos(theta)**2)**11.5*(2.92179207229736e+31*cos(theta)**2 - 5.96284096387217e+29)*sin(23*phi)

#@torch.jit.script
def Yl25_m_minus_22(theta, phi):
    return 1.37226189401167e-29*(1.0 - cos(theta)**2)**11*(9.73930690765788e+30*cos(theta)**3 - 5.96284096387217e+29*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl25_m_minus_21(theta, phi):
    return 1.88155071332724e-28*(1.0 - cos(theta)**2)**10.5*(2.43482672691447e+30*cos(theta)**4 - 2.98142048193609e+29*cos(theta)**2 + 3.17172391695328e+27)*sin(21*phi)

#@torch.jit.script
def Yl25_m_minus_20(theta, phi):
    return 2.85351294016536e-27*(1.0 - cos(theta)**2)**10*(4.86965345382894e+29*cos(theta)**5 - 9.93806827312028e+28*cos(theta)**3 + 3.17172391695328e+27*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl25_m_minus_19(theta, phi):
    return 4.68880021638437e-26*(1.0 - cos(theta)**2)**9.5*(8.1160890897149e+28*cos(theta)**6 - 2.48451706828007e+28*cos(theta)**4 + 1.58586195847664e+27*cos(theta)**2 - 1.17471256183455e+25)*sin(19*phi)

#@torch.jit.script
def Yl25_m_minus_18(theta, phi):
    return 8.22881098367386e-25*(1.0 - cos(theta)**2)**9*(1.1594412985307e+28*cos(theta)**7 - 4.96903413656014e+27*cos(theta)**5 + 5.28620652825547e+26*cos(theta)**3 - 1.17471256183455e+25*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl25_m_minus_17(theta, phi):
    return 1.52621707468272e-23*(1.0 - cos(theta)**2)**8.5*(1.44930162316337e+27*cos(theta)**8 - 8.28172356093357e+26*cos(theta)**6 + 1.32155163206387e+26*cos(theta)**4 - 5.87356280917274e+24*cos(theta)**2 + 3.41486209835625e+22)*sin(17*phi)

#@torch.jit.script
def Yl25_m_minus_16(theta, phi):
    return 2.96730513315039e-22*(1.0 - cos(theta)**2)**8*(1.61033513684819e+26*cos(theta)**9 - 1.18310336584765e+26*cos(theta)**7 + 2.64310326412774e+25*cos(theta)**5 - 1.95785426972425e+24*cos(theta)**3 + 3.41486209835625e+22*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl25_m_minus_15(theta, phi):
    return 6.00833495972093e-21*(1.0 - cos(theta)**2)**7.5*(1.61033513684819e+25*cos(theta)**10 - 1.47887920730957e+25*cos(theta)**8 + 4.40517210687956e+24*cos(theta)**6 - 4.89463567431062e+23*cos(theta)**4 + 1.70743104917812e+22*cos(theta)**2 - 8.32893194721036e+19)*sin(15*phi)

#@torch.jit.script
def Yl25_m_minus_14(theta, phi):
    return 1.26031897370507e-19*(1.0 - cos(theta)**2)**7*(1.46394103349836e+24*cos(theta)**11 - 1.64319911923285e+24*cos(theta)**9 + 6.29310300982794e+23*cos(theta)**7 - 9.78927134862124e+22*cos(theta)**5 + 5.69143683059375e+21*cos(theta)**3 - 8.32893194721036e+19*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl25_m_minus_13(theta, phi):
    return 2.72648680988027e-18*(1.0 - cos(theta)**2)**6.5*(1.21995086124863e+23*cos(theta)**12 - 1.64319911923285e+23*cos(theta)**10 + 7.86637876228493e+22*cos(theta)**8 - 1.63154522477021e+22*cos(theta)**6 + 1.42285920764844e+21*cos(theta)**4 - 4.16446597360518e+19*cos(theta)**2 + 1.77968631350649e+17)*sin(13*phi)

#@torch.jit.script
def Yl25_m_minus_12(theta, phi):
    return 6.05991978517773e-17*(1.0 - cos(theta)**2)**6*(9.38423739422025e+21*cos(theta)**13 - 1.49381738112077e+22*cos(theta)**11 + 8.74042084698325e+21*cos(theta)**9 - 2.33077889252887e+21*cos(theta)**7 + 2.84571841529687e+20*cos(theta)**5 - 1.38815532453506e+19*cos(theta)**3 + 1.77968631350649e+17*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl25_m_minus_11(theta, phi):
    return 1.37921431263761e-15*(1.0 - cos(theta)**2)**5.5*(6.70302671015732e+20*cos(theta)**14 - 1.24484781760064e+21*cos(theta)**12 + 8.74042084698325e+20*cos(theta)**10 - 2.91347361566108e+20*cos(theta)**8 + 4.74286402549479e+19*cos(theta)**6 - 3.47038831133765e+18*cos(theta)**4 + 8.89843156753244e+16*cos(theta)**2 - 343568786391214.0)*sin(11*phi)

#@torch.jit.script
def Yl25_m_minus_10(theta, phi):
    return 3.20500443821783e-14*(1.0 - cos(theta)**2)**5*(4.46868447343821e+19*cos(theta)**15 - 9.57575244308188e+19*cos(theta)**13 + 7.94583713362114e+19*cos(theta)**11 - 3.23719290629009e+19*cos(theta)**9 + 6.77552003642113e+18*cos(theta)**7 - 6.9407766226753e+17*cos(theta)**5 + 2.96614385584414e+16*cos(theta)**3 - 343568786391214.0*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl25_m_minus_9(theta, phi):
    return 7.58442478467402e-13*(1.0 - cos(theta)**2)**4.5*(2.79292779589888e+18*cos(theta)**16 - 6.83982317362992e+18*cos(theta)**14 + 6.62153094468428e+18*cos(theta)**12 - 3.23719290629009e+18*cos(theta)**10 + 8.46940004552641e+17*cos(theta)**8 - 1.15679610377922e+17*cos(theta)**6 + 7.41535963961036e+15*cos(theta)**4 - 171784393195607.0*cos(theta)**2 + 613515689984.31)*sin(9*phi)

#@torch.jit.script
def Yl25_m_minus_8(theta, phi):
    return 1.82341938685839e-11*(1.0 - cos(theta)**2)**4*(1.64289870346993e+17*cos(theta)**17 - 4.55988211575328e+17*cos(theta)**15 + 5.09348534206483e+17*cos(theta)**13 - 2.9429026420819e+17*cos(theta)**11 + 9.41044449502934e+16*cos(theta)**9 - 1.65256586254174e+16*cos(theta)**7 + 1.48307192792207e+15*cos(theta)**5 - 57261464398535.6*cos(theta)**3 + 613515689984.31*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl25_m_minus_7(theta, phi):
    return 4.44405873797859e-10*(1.0 - cos(theta)**2)**3.5*(9.12721501927739e+15*cos(theta)**18 - 2.8499263223458e+16*cos(theta)**16 + 3.63820381576059e+16*cos(theta)**14 - 2.45241886840159e+16*cos(theta)**12 + 9.41044449502934e+15*cos(theta)**10 - 2.06570732817717e+15*cos(theta)**8 + 247178654653679.0*cos(theta)**6 - 14315366099633.9*cos(theta)**4 + 306757844992.155*cos(theta)**2 - 1032854696.94328)*sin(7*phi)

#@torch.jit.script
def Yl25_m_minus_6(theta, phi):
    return 1.09580071657648e-8*(1.0 - cos(theta)**2)**3*(480379737856705.0*cos(theta)**19 - 1.67642724843871e+15*cos(theta)**17 + 2.42546921050706e+15*cos(theta)**15 - 1.8864760526166e+15*cos(theta)**13 + 855494954093576.0*cos(theta)**11 - 229523036464130.0*cos(theta)**9 + 35311236379097.0*cos(theta)**7 - 2863073219926.78*cos(theta)**5 + 102252614997.385*cos(theta)**3 - 1032854696.94328*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl25_m_minus_5(theta, phi):
    return 2.72852178015624e-7*(1.0 - cos(theta)**2)**2.5*(24018986892835.3*cos(theta)**20 - 93134847135483.6*cos(theta)**18 + 151591825656691.0*cos(theta)**16 - 134748289472615.0*cos(theta)**14 + 71291246174464.7*cos(theta)**12 - 22952303646413.0*cos(theta)**10 + 4413904547387.12*cos(theta)**8 - 477178869987.797*cos(theta)**6 + 25563153749.3463*cos(theta)**4 - 516427348.471642*cos(theta)**2 + 1665894.67248917)*sin(5*phi)

#@torch.jit.script
def Yl25_m_minus_4(theta, phi):
    return 6.84853531495298e-6*(1.0 - cos(theta)**2)**2*(1143761280611.2*cos(theta)**21 - 4901834059762.3*cos(theta)**19 + 8917166215099.5*cos(theta)**17 - 8983219298174.31*cos(theta)**15 + 5483942013420.36*cos(theta)**13 - 2086573058764.82*cos(theta)**11 + 490433838598.569*cos(theta)**9 - 68168409998.2567*cos(theta)**7 + 5112630749.86925*cos(theta)**5 - 172142449.490547*cos(theta)**3 + 1665894.67248917*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl25_m_minus_3(theta, phi):
    return 0.000172984837897952*(1.0 - cos(theta)**2)**1.5*(51989149118.691*cos(theta)**22 - 245091702988.115*cos(theta)**20 + 495398123061.083*cos(theta)**18 - 561451206135.894*cos(theta)**16 + 391710143815.74*cos(theta)**14 - 173881088230.402*cos(theta)**12 + 49043383859.8569*cos(theta)**10 - 8521051249.78209*cos(theta)**8 + 852105124.978209*cos(theta)**6 - 43035612.3726368*cos(theta)**4 + 832947.336244583*cos(theta)**2 - 2611.12017631531)*sin(3*phi)

#@torch.jit.script
def Yl25_m_minus_2(theta, phi):
    return 0.00438986305798052*(1.0 - cos(theta)**2)*(2260397787.76917*cos(theta)**23 - 11671033475.6245*cos(theta)**21 + 26073585424.2675*cos(theta)**19 - 33026541537.4055*cos(theta)**17 + 26114009587.716*cos(theta)**15 - 13375468325.4155*cos(theta)**13 + 4458489441.80517*cos(theta)**11 - 946783472.198009*cos(theta)**9 + 121729303.568316*cos(theta)**7 - 8607122.47452736*cos(theta)**5 + 277649.112081528*cos(theta)**3 - 2611.12017631531*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl25_m_minus_1(theta, phi):
    return 0.11174766972402*(1.0 - cos(theta)**2)**0.5*(94183241.1570489*cos(theta)**24 - 530501521.619296*cos(theta)**22 + 1303679271.21338*cos(theta)**20 - 1834807863.1892*cos(theta)**18 + 1632125599.23225*cos(theta)**16 - 955390594.672537*cos(theta)**14 + 371540786.817098*cos(theta)**12 - 94678347.2198009*cos(theta)**10 + 15216162.9460394*cos(theta)**8 - 1434520.41242123*cos(theta)**6 + 69412.2780203819*cos(theta)**4 - 1305.56008815765*cos(theta)**2 + 4.02950644493103)*sin(phi)

#@torch.jit.script
def Yl25_m0(theta, phi):
    return 23843151.1500716*cos(theta)**25 - 145978476.42901*cos(theta)**23 + 392899516.346165*cos(theta)**21 - 611177025.427368*cos(theta)**19 + 607623670.628372*cos(theta)**17 - 403106435.148578*cos(theta)**15 + 180881092.694875*cos(theta)**13 - 54473842.5876457*cos(theta)**11 + 10700219.0797161*cos(theta)**9 - 1296996.2520868*cos(theta)**7 + 87861.0364316867*cos(theta)**5 - 2754.26446494316*cos(theta)**3 + 25.5024487494737*cos(theta)

#@torch.jit.script
def Yl25_m1(theta, phi):
    return 0.11174766972402*(1.0 - cos(theta)**2)**0.5*(94183241.1570489*cos(theta)**24 - 530501521.619296*cos(theta)**22 + 1303679271.21338*cos(theta)**20 - 1834807863.1892*cos(theta)**18 + 1632125599.23225*cos(theta)**16 - 955390594.672537*cos(theta)**14 + 371540786.817098*cos(theta)**12 - 94678347.2198009*cos(theta)**10 + 15216162.9460394*cos(theta)**8 - 1434520.41242123*cos(theta)**6 + 69412.2780203819*cos(theta)**4 - 1305.56008815765*cos(theta)**2 + 4.02950644493103)*cos(phi)

#@torch.jit.script
def Yl25_m2(theta, phi):
    return 0.00438986305798052*(1.0 - cos(theta)**2)*(2260397787.76917*cos(theta)**23 - 11671033475.6245*cos(theta)**21 + 26073585424.2675*cos(theta)**19 - 33026541537.4055*cos(theta)**17 + 26114009587.716*cos(theta)**15 - 13375468325.4155*cos(theta)**13 + 4458489441.80517*cos(theta)**11 - 946783472.198009*cos(theta)**9 + 121729303.568316*cos(theta)**7 - 8607122.47452736*cos(theta)**5 + 277649.112081528*cos(theta)**3 - 2611.12017631531*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl25_m3(theta, phi):
    return 0.000172984837897952*(1.0 - cos(theta)**2)**1.5*(51989149118.691*cos(theta)**22 - 245091702988.115*cos(theta)**20 + 495398123061.083*cos(theta)**18 - 561451206135.894*cos(theta)**16 + 391710143815.74*cos(theta)**14 - 173881088230.402*cos(theta)**12 + 49043383859.8569*cos(theta)**10 - 8521051249.78209*cos(theta)**8 + 852105124.978209*cos(theta)**6 - 43035612.3726368*cos(theta)**4 + 832947.336244583*cos(theta)**2 - 2611.12017631531)*cos(3*phi)

#@torch.jit.script
def Yl25_m4(theta, phi):
    return 6.84853531495298e-6*(1.0 - cos(theta)**2)**2*(1143761280611.2*cos(theta)**21 - 4901834059762.3*cos(theta)**19 + 8917166215099.5*cos(theta)**17 - 8983219298174.31*cos(theta)**15 + 5483942013420.36*cos(theta)**13 - 2086573058764.82*cos(theta)**11 + 490433838598.569*cos(theta)**9 - 68168409998.2567*cos(theta)**7 + 5112630749.86925*cos(theta)**5 - 172142449.490547*cos(theta)**3 + 1665894.67248917*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl25_m5(theta, phi):
    return 2.72852178015624e-7*(1.0 - cos(theta)**2)**2.5*(24018986892835.3*cos(theta)**20 - 93134847135483.6*cos(theta)**18 + 151591825656691.0*cos(theta)**16 - 134748289472615.0*cos(theta)**14 + 71291246174464.7*cos(theta)**12 - 22952303646413.0*cos(theta)**10 + 4413904547387.12*cos(theta)**8 - 477178869987.797*cos(theta)**6 + 25563153749.3463*cos(theta)**4 - 516427348.471642*cos(theta)**2 + 1665894.67248917)*cos(5*phi)

#@torch.jit.script
def Yl25_m6(theta, phi):
    return 1.09580071657648e-8*(1.0 - cos(theta)**2)**3*(480379737856705.0*cos(theta)**19 - 1.67642724843871e+15*cos(theta)**17 + 2.42546921050706e+15*cos(theta)**15 - 1.8864760526166e+15*cos(theta)**13 + 855494954093576.0*cos(theta)**11 - 229523036464130.0*cos(theta)**9 + 35311236379097.0*cos(theta)**7 - 2863073219926.78*cos(theta)**5 + 102252614997.385*cos(theta)**3 - 1032854696.94328*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl25_m7(theta, phi):
    return 4.44405873797859e-10*(1.0 - cos(theta)**2)**3.5*(9.12721501927739e+15*cos(theta)**18 - 2.8499263223458e+16*cos(theta)**16 + 3.63820381576059e+16*cos(theta)**14 - 2.45241886840159e+16*cos(theta)**12 + 9.41044449502934e+15*cos(theta)**10 - 2.06570732817717e+15*cos(theta)**8 + 247178654653679.0*cos(theta)**6 - 14315366099633.9*cos(theta)**4 + 306757844992.155*cos(theta)**2 - 1032854696.94328)*cos(7*phi)

#@torch.jit.script
def Yl25_m8(theta, phi):
    return 1.82341938685839e-11*(1.0 - cos(theta)**2)**4*(1.64289870346993e+17*cos(theta)**17 - 4.55988211575328e+17*cos(theta)**15 + 5.09348534206483e+17*cos(theta)**13 - 2.9429026420819e+17*cos(theta)**11 + 9.41044449502934e+16*cos(theta)**9 - 1.65256586254174e+16*cos(theta)**7 + 1.48307192792207e+15*cos(theta)**5 - 57261464398535.6*cos(theta)**3 + 613515689984.31*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl25_m9(theta, phi):
    return 7.58442478467402e-13*(1.0 - cos(theta)**2)**4.5*(2.79292779589888e+18*cos(theta)**16 - 6.83982317362992e+18*cos(theta)**14 + 6.62153094468428e+18*cos(theta)**12 - 3.23719290629009e+18*cos(theta)**10 + 8.46940004552641e+17*cos(theta)**8 - 1.15679610377922e+17*cos(theta)**6 + 7.41535963961036e+15*cos(theta)**4 - 171784393195607.0*cos(theta)**2 + 613515689984.31)*cos(9*phi)

#@torch.jit.script
def Yl25_m10(theta, phi):
    return 3.20500443821783e-14*(1.0 - cos(theta)**2)**5*(4.46868447343821e+19*cos(theta)**15 - 9.57575244308188e+19*cos(theta)**13 + 7.94583713362114e+19*cos(theta)**11 - 3.23719290629009e+19*cos(theta)**9 + 6.77552003642113e+18*cos(theta)**7 - 6.9407766226753e+17*cos(theta)**5 + 2.96614385584414e+16*cos(theta)**3 - 343568786391214.0*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl25_m11(theta, phi):
    return 1.37921431263761e-15*(1.0 - cos(theta)**2)**5.5*(6.70302671015732e+20*cos(theta)**14 - 1.24484781760064e+21*cos(theta)**12 + 8.74042084698325e+20*cos(theta)**10 - 2.91347361566108e+20*cos(theta)**8 + 4.74286402549479e+19*cos(theta)**6 - 3.47038831133765e+18*cos(theta)**4 + 8.89843156753244e+16*cos(theta)**2 - 343568786391214.0)*cos(11*phi)

#@torch.jit.script
def Yl25_m12(theta, phi):
    return 6.05991978517773e-17*(1.0 - cos(theta)**2)**6*(9.38423739422025e+21*cos(theta)**13 - 1.49381738112077e+22*cos(theta)**11 + 8.74042084698325e+21*cos(theta)**9 - 2.33077889252887e+21*cos(theta)**7 + 2.84571841529687e+20*cos(theta)**5 - 1.38815532453506e+19*cos(theta)**3 + 1.77968631350649e+17*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl25_m13(theta, phi):
    return 2.72648680988027e-18*(1.0 - cos(theta)**2)**6.5*(1.21995086124863e+23*cos(theta)**12 - 1.64319911923285e+23*cos(theta)**10 + 7.86637876228493e+22*cos(theta)**8 - 1.63154522477021e+22*cos(theta)**6 + 1.42285920764844e+21*cos(theta)**4 - 4.16446597360518e+19*cos(theta)**2 + 1.77968631350649e+17)*cos(13*phi)

#@torch.jit.script
def Yl25_m14(theta, phi):
    return 1.26031897370507e-19*(1.0 - cos(theta)**2)**7*(1.46394103349836e+24*cos(theta)**11 - 1.64319911923285e+24*cos(theta)**9 + 6.29310300982794e+23*cos(theta)**7 - 9.78927134862124e+22*cos(theta)**5 + 5.69143683059375e+21*cos(theta)**3 - 8.32893194721036e+19*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl25_m15(theta, phi):
    return 6.00833495972093e-21*(1.0 - cos(theta)**2)**7.5*(1.61033513684819e+25*cos(theta)**10 - 1.47887920730957e+25*cos(theta)**8 + 4.40517210687956e+24*cos(theta)**6 - 4.89463567431062e+23*cos(theta)**4 + 1.70743104917812e+22*cos(theta)**2 - 8.32893194721036e+19)*cos(15*phi)

#@torch.jit.script
def Yl25_m16(theta, phi):
    return 2.96730513315039e-22*(1.0 - cos(theta)**2)**8*(1.61033513684819e+26*cos(theta)**9 - 1.18310336584765e+26*cos(theta)**7 + 2.64310326412774e+25*cos(theta)**5 - 1.95785426972425e+24*cos(theta)**3 + 3.41486209835625e+22*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl25_m17(theta, phi):
    return 1.52621707468272e-23*(1.0 - cos(theta)**2)**8.5*(1.44930162316337e+27*cos(theta)**8 - 8.28172356093357e+26*cos(theta)**6 + 1.32155163206387e+26*cos(theta)**4 - 5.87356280917274e+24*cos(theta)**2 + 3.41486209835625e+22)*cos(17*phi)

#@torch.jit.script
def Yl25_m18(theta, phi):
    return 8.22881098367386e-25*(1.0 - cos(theta)**2)**9*(1.1594412985307e+28*cos(theta)**7 - 4.96903413656014e+27*cos(theta)**5 + 5.28620652825547e+26*cos(theta)**3 - 1.17471256183455e+25*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl25_m19(theta, phi):
    return 4.68880021638437e-26*(1.0 - cos(theta)**2)**9.5*(8.1160890897149e+28*cos(theta)**6 - 2.48451706828007e+28*cos(theta)**4 + 1.58586195847664e+27*cos(theta)**2 - 1.17471256183455e+25)*cos(19*phi)

#@torch.jit.script
def Yl25_m20(theta, phi):
    return 2.85351294016536e-27*(1.0 - cos(theta)**2)**10*(4.86965345382894e+29*cos(theta)**5 - 9.93806827312028e+28*cos(theta)**3 + 3.17172391695328e+27*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl25_m21(theta, phi):
    return 1.88155071332724e-28*(1.0 - cos(theta)**2)**10.5*(2.43482672691447e+30*cos(theta)**4 - 2.98142048193609e+29*cos(theta)**2 + 3.17172391695328e+27)*cos(21*phi)

#@torch.jit.script
def Yl25_m22(theta, phi):
    return 1.37226189401167e-29*(1.0 - cos(theta)**2)**11*(9.73930690765788e+30*cos(theta)**3 - 5.96284096387217e+29*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl25_m23(theta, phi):
    return 1.14355157834306e-30*(1.0 - cos(theta)**2)**11.5*(2.92179207229736e+31*cos(theta)**2 - 5.96284096387217e+29)*cos(23*phi)

#@torch.jit.script
def Yl25_m24(theta, phi):
    return 6.75028364024702*(1.0 - cos(theta)**2)**12*cos(24*phi)*cos(theta)

#@torch.jit.script
def Yl25_m25(theta, phi):
    return 0.954634267390256*(1.0 - cos(theta)**2)**12.5*cos(25*phi)

#@torch.jit.script
def Yl26_m_minus_26(theta, phi):
    return 0.963769731686801*(1.0 - cos(theta)**2)**13*sin(26*phi)

#@torch.jit.script
def Yl26_m_minus_25(theta, phi):
    return 6.94984237067387*(1.0 - cos(theta)**2)**12.5*sin(25*phi)*cos(theta)

#@torch.jit.script
def Yl26_m_minus_24(theta, phi):
    return 2.35518790424645e-32*(1.0 - cos(theta)**2)**12*(1.49011395687166e+33*cos(theta)**2 - 2.92179207229736e+31)*sin(24*phi)

#@torch.jit.script
def Yl26_m_minus_23(theta, phi):
    return 2.88450430688934e-31*(1.0 - cos(theta)**2)**11.5*(4.96704652290552e+32*cos(theta)**3 - 2.92179207229736e+31*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl26_m_minus_22(theta, phi):
    return 4.03830602964508e-30*(1.0 - cos(theta)**2)**11*(1.24176163072638e+32*cos(theta)**4 - 1.46089603614868e+31*cos(theta)**2 + 1.49071024096804e+29)*sin(22*phi)

#@torch.jit.script
def Yl26_m_minus_21(theta, phi):
    return 6.25611679988175e-29*(1.0 - cos(theta)**2)**10.5*(2.48352326145276e+31*cos(theta)**5 - 4.86965345382894e+30*cos(theta)**3 + 1.49071024096804e+29*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl26_m_minus_20(theta, phi):
    return 1.0505806618571e-27*(1.0 - cos(theta)**2)**10*(4.1392054357546e+30*cos(theta)**6 - 1.21741336345723e+30*cos(theta)**4 + 7.45355120484021e+28*cos(theta)**2 - 5.28620652825547e+26)*sin(20*phi)

#@torch.jit.script
def Yl26_m_minus_19(theta, phi):
    return 1.88519959716718e-26*(1.0 - cos(theta)**2)**9.5*(5.91315062250657e+29*cos(theta)**7 - 2.43482672691447e+29*cos(theta)**5 + 2.48451706828007e+28*cos(theta)**3 - 5.28620652825547e+26*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl26_m_minus_18(theta, phi):
    return 3.57691474264813e-25*(1.0 - cos(theta)**2)**9*(7.39143827813321e+28*cos(theta)**8 - 4.05804454485745e+28*cos(theta)**6 + 6.21129267070018e+27*cos(theta)**4 - 2.64310326412774e+26*cos(theta)**2 + 1.46839070229319e+24)*sin(18*phi)

#@torch.jit.script
def Yl26_m_minus_17(theta, phi):
    return 7.11797046507269e-24*(1.0 - cos(theta)**2)**8.5*(8.21270919792579e+27*cos(theta)**9 - 5.7972064926535e+27*cos(theta)**7 + 1.24225853414004e+27*cos(theta)**5 - 8.81034421375912e+25*cos(theta)**3 + 1.46839070229319e+24*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl26_m_minus_16(theta, phi):
    return 1.47601377103699e-22*(1.0 - cos(theta)**2)**8*(8.21270919792579e+26*cos(theta)**10 - 7.24650811581687e+26*cos(theta)**8 + 2.07043089023339e+26*cos(theta)**6 - 2.20258605343978e+25*cos(theta)**4 + 7.34195351146593e+23*cos(theta)**2 - 3.41486209835625e+21)*sin(16*phi)

#@torch.jit.script
def Yl26_m_minus_15(theta, phi):
    return 3.17257134412823e-21*(1.0 - cos(theta)**2)**7.5*(7.46609927084163e+25*cos(theta)**11 - 8.05167568424097e+25*cos(theta)**9 + 2.95775841461913e+25*cos(theta)**7 - 4.40517210687956e+24*cos(theta)**5 + 2.44731783715531e+23*cos(theta)**3 - 3.41486209835625e+21*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl26_m_minus_14(theta, phi):
    return 7.03710366224851e-20*(1.0 - cos(theta)**2)**7*(6.22174939236802e+24*cos(theta)**12 - 8.05167568424097e+24*cos(theta)**10 + 3.69719801827392e+24*cos(theta)**8 - 7.34195351146593e+23*cos(theta)**6 + 6.11829459288828e+22*cos(theta)**4 - 1.70743104917812e+21*cos(theta)**2 + 6.9407766226753e+18)*sin(14*phi)

#@torch.jit.script
def Yl26_m_minus_13(theta, phi):
    return 1.60470653191418e-18*(1.0 - cos(theta)**2)**6.5*(4.78596107105233e+23*cos(theta)**13 - 7.31970516749179e+23*cos(theta)**11 + 4.10799779808213e+23*cos(theta)**9 - 1.04885050163799e+23*cos(theta)**7 + 1.22365891857766e+22*cos(theta)**5 - 5.69143683059374e+20*cos(theta)**3 + 6.9407766226753e+18*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl26_m_minus_12(theta, phi):
    return 3.74966044762475e-17*(1.0 - cos(theta)**2)**6*(3.41854362218023e+22*cos(theta)**14 - 6.09975430624316e+22*cos(theta)**12 + 4.10799779808213e+22*cos(theta)**10 - 1.31106312704749e+22*cos(theta)**8 + 2.03943153096276e+21*cos(theta)**6 - 1.42285920764844e+20*cos(theta)**4 + 3.47038831133765e+18*cos(theta)**2 - 1.27120450964749e+16)*sin(12*phi)

#@torch.jit.script
def Yl26_m_minus_11(theta, phi):
    return 8.95219161955017e-16*(1.0 - cos(theta)**2)**5.5*(2.27902908145349e+21*cos(theta)**15 - 4.69211869711012e+21*cos(theta)**13 + 3.73454345280193e+21*cos(theta)**11 - 1.45673680783054e+21*cos(theta)**9 + 2.91347361566108e+20*cos(theta)**7 - 2.84571841529687e+19*cos(theta)**5 + 1.15679610377922e+18*cos(theta)**3 - 1.27120450964749e+16*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl26_m_minus_10(theta, phi):
    return 2.17816222989798e-14*(1.0 - cos(theta)**2)**5*(1.42439317590843e+20*cos(theta)**16 - 3.35151335507866e+20*cos(theta)**14 + 3.11211954400161e+20*cos(theta)**12 - 1.45673680783054e+20*cos(theta)**10 + 3.64184201957635e+19*cos(theta)**8 - 4.74286402549479e+18*cos(theta)**6 + 2.89199025944804e+17*cos(theta)**4 - 6.35602254823745e+15*cos(theta)**2 + 21473049149450.9)*sin(10*phi)

#@torch.jit.script
def Yl26_m_minus_9(theta, phi):
    return 5.38847576616016e-13*(1.0 - cos(theta)**2)**4.5*(8.37878338769665e+18*cos(theta)**17 - 2.23434223671911e+19*cos(theta)**15 + 2.39393811077047e+19*cos(theta)**13 - 1.32430618893686e+19*cos(theta)**11 + 4.04649113286262e+18*cos(theta)**9 - 6.77552003642113e+17*cos(theta)**7 + 5.78398051889608e+16*cos(theta)**5 - 2.11867418274582e+15*cos(theta)**3 + 21473049149450.9*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl26_m_minus_8(theta, phi):
    return 1.35249668324814e-11*(1.0 - cos(theta)**2)**4*(4.65487965983147e+17*cos(theta)**18 - 1.39646389794944e+18*cos(theta)**16 + 1.70995579340748e+18*cos(theta)**14 - 1.10358849078071e+18*cos(theta)**12 + 4.04649113286262e+17*cos(theta)**10 - 8.46940004552641e+16*cos(theta)**8 + 9.63996753149347e+15*cos(theta)**6 - 529668545686454.0*cos(theta)**4 + 10736524574725.4*cos(theta)**2 - 34084204999.1283)*sin(8*phi)

#@torch.jit.script
def Yl26_m_minus_7(theta, phi):
    return 3.43757725980871e-10*(1.0 - cos(theta)**2)**3.5*(2.4499366630692e+16*cos(theta)**19 - 8.21449351734965e+16*cos(theta)**17 + 1.13997052893832e+17*cos(theta)**15 - 8.48914223677472e+16*cos(theta)**13 + 3.67862830260238e+16*cos(theta)**11 - 9.41044449502934e+15*cos(theta)**9 + 1.37713821878478e+15*cos(theta)**7 - 105933709137291.0*cos(theta)**5 + 3578841524908.48*cos(theta)**3 - 34084204999.1283*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl26_m_minus_6(theta, phi):
    return 8.83129588187465e-9*(1.0 - cos(theta)**2)**3*(1.2249683315346e+15*cos(theta)**20 - 4.5636075096387e+15*cos(theta)**18 + 7.1248158058645e+15*cos(theta)**16 - 6.06367302626766e+15*cos(theta)**14 + 3.06552358550198e+15*cos(theta)**12 - 941044449502934.0*cos(theta)**10 + 172142277348098.0*cos(theta)**8 - 17655618189548.5*cos(theta)**6 + 894710381227.119*cos(theta)**4 - 17042102499.5642*cos(theta)**2 + 51642734.8471642)*sin(6*phi)

#@torch.jit.script
def Yl26_m_minus_5(theta, phi):
    return 2.28933354565387e-7*(1.0 - cos(theta)**2)**2.5*(58331825311171.3*cos(theta)**21 - 240189868928353.0*cos(theta)**19 + 419106812109676.0*cos(theta)**17 - 404244868417844.0*cos(theta)**15 + 235809506577076.0*cos(theta)**13 - 85549495409357.6*cos(theta)**11 + 19126919705344.2*cos(theta)**9 - 2522231169935.5*cos(theta)**7 + 178942076245.424*cos(theta)**5 - 5680700833.18806*cos(theta)**3 + 51642734.8471642*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl26_m_minus_4(theta, phi):
    return 5.97862425042808e-6*(1.0 - cos(theta)**2)**2*(2651446605053.24*cos(theta)**22 - 12009493446417.6*cos(theta)**20 + 23283711783870.9*cos(theta)**18 - 25265304276115.2*cos(theta)**16 + 16843536184076.8*cos(theta)**14 - 7129124617446.47*cos(theta)**12 + 1912691970534.42*cos(theta)**10 - 315278896241.937*cos(theta)**8 + 29823679374.2373*cos(theta)**6 - 1420175208.29701*cos(theta)**4 + 25821367.4235821*cos(theta)**2 - 75722.4851131439)*sin(4*phi)

#@torch.jit.script
def Yl26_m_minus_3(theta, phi):
    return 0.000157045611432433*(1.0 - cos(theta)**2)**1.5*(115280287176.228*cos(theta)**23 - 571880640305.601*cos(theta)**21 + 1225458514940.57*cos(theta)**19 - 1486194369183.25*cos(theta)**17 + 1122902412271.79*cos(theta)**15 - 548394201342.036*cos(theta)**13 + 173881088230.402*cos(theta)**11 - 35030988471.3264*cos(theta)**9 + 4260525624.89104*cos(theta)**7 - 284035041.659403*cos(theta)**5 + 8607122.47452736*cos(theta)**3 - 75722.4851131439*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl26_m_minus_2(theta, phi):
    return 0.00414314778312938*(1.0 - cos(theta)**2)*(4803345299.0095*cos(theta)**24 - 25994574559.3455*cos(theta)**22 + 61272925747.0287*cos(theta)**20 - 82566353843.5138*cos(theta)**18 + 70181400766.9868*cos(theta)**16 - 39171014381.574*cos(theta)**14 + 14490090685.8668*cos(theta)**12 - 3503098847.13264*cos(theta)**10 + 532565703.11138*cos(theta)**8 - 47339173.6099005*cos(theta)**6 + 2151780.61863184*cos(theta)**4 - 37861.242556572*cos(theta)**2 + 108.796674013138)*sin(2*phi)

#@torch.jit.script
def Yl26_m_minus_1(theta, phi):
    return 0.109617386791489*(1.0 - cos(theta)**2)**0.5*(192133811.96038*cos(theta)**25 - 1130198893.88459*cos(theta)**23 + 2917758368.90613*cos(theta)**21 - 4345597570.71126*cos(theta)**19 + 4128317692.17569*cos(theta)**17 - 2611400958.7716*cos(theta)**15 + 1114622360.45129*cos(theta)**13 - 318463531.557512*cos(theta)**11 + 59173967.0123756*cos(theta)**9 - 6762739.08712864*cos(theta)**7 + 430356.123726368*cos(theta)**5 - 12620.414185524*cos(theta)**3 + 108.796674013138*cos(theta))*sin(phi)

#@torch.jit.script
def Yl26_m0(theta, phi):
    return 47677483.75133*cos(theta)**26 - 303827102.336907*cos(theta)**24 + 855676329.030472*cos(theta)**22 - 1401852709.26269*cos(theta)**20 + 1479733415.33284*cos(theta)**18 - 1053019593.23686*cos(theta)**16 + 513668094.261881*cos(theta)**14 - 171222698.087294*cos(theta)**12 + 38178034.0329777*cos(theta)**10 - 5454004.86185395*cos(theta)**8 + 462764.048884578*cos(theta)**6 - 20356.1898336325*cos(theta)**4 + 350.968790235042*cos(theta)**2 - 0.999911083290719

#@torch.jit.script
def Yl26_m1(theta, phi):
    return 0.109617386791489*(1.0 - cos(theta)**2)**0.5*(192133811.96038*cos(theta)**25 - 1130198893.88459*cos(theta)**23 + 2917758368.90613*cos(theta)**21 - 4345597570.71126*cos(theta)**19 + 4128317692.17569*cos(theta)**17 - 2611400958.7716*cos(theta)**15 + 1114622360.45129*cos(theta)**13 - 318463531.557512*cos(theta)**11 + 59173967.0123756*cos(theta)**9 - 6762739.08712864*cos(theta)**7 + 430356.123726368*cos(theta)**5 - 12620.414185524*cos(theta)**3 + 108.796674013138*cos(theta))*cos(phi)

#@torch.jit.script
def Yl26_m2(theta, phi):
    return 0.00414314778312938*(1.0 - cos(theta)**2)*(4803345299.0095*cos(theta)**24 - 25994574559.3455*cos(theta)**22 + 61272925747.0287*cos(theta)**20 - 82566353843.5138*cos(theta)**18 + 70181400766.9868*cos(theta)**16 - 39171014381.574*cos(theta)**14 + 14490090685.8668*cos(theta)**12 - 3503098847.13264*cos(theta)**10 + 532565703.11138*cos(theta)**8 - 47339173.6099005*cos(theta)**6 + 2151780.61863184*cos(theta)**4 - 37861.242556572*cos(theta)**2 + 108.796674013138)*cos(2*phi)

#@torch.jit.script
def Yl26_m3(theta, phi):
    return 0.000157045611432433*(1.0 - cos(theta)**2)**1.5*(115280287176.228*cos(theta)**23 - 571880640305.601*cos(theta)**21 + 1225458514940.57*cos(theta)**19 - 1486194369183.25*cos(theta)**17 + 1122902412271.79*cos(theta)**15 - 548394201342.036*cos(theta)**13 + 173881088230.402*cos(theta)**11 - 35030988471.3264*cos(theta)**9 + 4260525624.89104*cos(theta)**7 - 284035041.659403*cos(theta)**5 + 8607122.47452736*cos(theta)**3 - 75722.4851131439*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl26_m4(theta, phi):
    return 5.97862425042808e-6*(1.0 - cos(theta)**2)**2*(2651446605053.24*cos(theta)**22 - 12009493446417.6*cos(theta)**20 + 23283711783870.9*cos(theta)**18 - 25265304276115.2*cos(theta)**16 + 16843536184076.8*cos(theta)**14 - 7129124617446.47*cos(theta)**12 + 1912691970534.42*cos(theta)**10 - 315278896241.937*cos(theta)**8 + 29823679374.2373*cos(theta)**6 - 1420175208.29701*cos(theta)**4 + 25821367.4235821*cos(theta)**2 - 75722.4851131439)*cos(4*phi)

#@torch.jit.script
def Yl26_m5(theta, phi):
    return 2.28933354565387e-7*(1.0 - cos(theta)**2)**2.5*(58331825311171.3*cos(theta)**21 - 240189868928353.0*cos(theta)**19 + 419106812109676.0*cos(theta)**17 - 404244868417844.0*cos(theta)**15 + 235809506577076.0*cos(theta)**13 - 85549495409357.6*cos(theta)**11 + 19126919705344.2*cos(theta)**9 - 2522231169935.5*cos(theta)**7 + 178942076245.424*cos(theta)**5 - 5680700833.18806*cos(theta)**3 + 51642734.8471642*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl26_m6(theta, phi):
    return 8.83129588187465e-9*(1.0 - cos(theta)**2)**3*(1.2249683315346e+15*cos(theta)**20 - 4.5636075096387e+15*cos(theta)**18 + 7.1248158058645e+15*cos(theta)**16 - 6.06367302626766e+15*cos(theta)**14 + 3.06552358550198e+15*cos(theta)**12 - 941044449502934.0*cos(theta)**10 + 172142277348098.0*cos(theta)**8 - 17655618189548.5*cos(theta)**6 + 894710381227.119*cos(theta)**4 - 17042102499.5642*cos(theta)**2 + 51642734.8471642)*cos(6*phi)

#@torch.jit.script
def Yl26_m7(theta, phi):
    return 3.43757725980871e-10*(1.0 - cos(theta)**2)**3.5*(2.4499366630692e+16*cos(theta)**19 - 8.21449351734965e+16*cos(theta)**17 + 1.13997052893832e+17*cos(theta)**15 - 8.48914223677472e+16*cos(theta)**13 + 3.67862830260238e+16*cos(theta)**11 - 9.41044449502934e+15*cos(theta)**9 + 1.37713821878478e+15*cos(theta)**7 - 105933709137291.0*cos(theta)**5 + 3578841524908.48*cos(theta)**3 - 34084204999.1283*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl26_m8(theta, phi):
    return 1.35249668324814e-11*(1.0 - cos(theta)**2)**4*(4.65487965983147e+17*cos(theta)**18 - 1.39646389794944e+18*cos(theta)**16 + 1.70995579340748e+18*cos(theta)**14 - 1.10358849078071e+18*cos(theta)**12 + 4.04649113286262e+17*cos(theta)**10 - 8.46940004552641e+16*cos(theta)**8 + 9.63996753149347e+15*cos(theta)**6 - 529668545686454.0*cos(theta)**4 + 10736524574725.4*cos(theta)**2 - 34084204999.1283)*cos(8*phi)

#@torch.jit.script
def Yl26_m9(theta, phi):
    return 5.38847576616016e-13*(1.0 - cos(theta)**2)**4.5*(8.37878338769665e+18*cos(theta)**17 - 2.23434223671911e+19*cos(theta)**15 + 2.39393811077047e+19*cos(theta)**13 - 1.32430618893686e+19*cos(theta)**11 + 4.04649113286262e+18*cos(theta)**9 - 6.77552003642113e+17*cos(theta)**7 + 5.78398051889608e+16*cos(theta)**5 - 2.11867418274582e+15*cos(theta)**3 + 21473049149450.9*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl26_m10(theta, phi):
    return 2.17816222989798e-14*(1.0 - cos(theta)**2)**5*(1.42439317590843e+20*cos(theta)**16 - 3.35151335507866e+20*cos(theta)**14 + 3.11211954400161e+20*cos(theta)**12 - 1.45673680783054e+20*cos(theta)**10 + 3.64184201957635e+19*cos(theta)**8 - 4.74286402549479e+18*cos(theta)**6 + 2.89199025944804e+17*cos(theta)**4 - 6.35602254823745e+15*cos(theta)**2 + 21473049149450.9)*cos(10*phi)

#@torch.jit.script
def Yl26_m11(theta, phi):
    return 8.95219161955017e-16*(1.0 - cos(theta)**2)**5.5*(2.27902908145349e+21*cos(theta)**15 - 4.69211869711012e+21*cos(theta)**13 + 3.73454345280193e+21*cos(theta)**11 - 1.45673680783054e+21*cos(theta)**9 + 2.91347361566108e+20*cos(theta)**7 - 2.84571841529687e+19*cos(theta)**5 + 1.15679610377922e+18*cos(theta)**3 - 1.27120450964749e+16*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl26_m12(theta, phi):
    return 3.74966044762475e-17*(1.0 - cos(theta)**2)**6*(3.41854362218023e+22*cos(theta)**14 - 6.09975430624316e+22*cos(theta)**12 + 4.10799779808213e+22*cos(theta)**10 - 1.31106312704749e+22*cos(theta)**8 + 2.03943153096276e+21*cos(theta)**6 - 1.42285920764844e+20*cos(theta)**4 + 3.47038831133765e+18*cos(theta)**2 - 1.27120450964749e+16)*cos(12*phi)

#@torch.jit.script
def Yl26_m13(theta, phi):
    return 1.60470653191418e-18*(1.0 - cos(theta)**2)**6.5*(4.78596107105233e+23*cos(theta)**13 - 7.31970516749179e+23*cos(theta)**11 + 4.10799779808213e+23*cos(theta)**9 - 1.04885050163799e+23*cos(theta)**7 + 1.22365891857766e+22*cos(theta)**5 - 5.69143683059374e+20*cos(theta)**3 + 6.9407766226753e+18*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl26_m14(theta, phi):
    return 7.03710366224851e-20*(1.0 - cos(theta)**2)**7*(6.22174939236802e+24*cos(theta)**12 - 8.05167568424097e+24*cos(theta)**10 + 3.69719801827392e+24*cos(theta)**8 - 7.34195351146593e+23*cos(theta)**6 + 6.11829459288828e+22*cos(theta)**4 - 1.70743104917812e+21*cos(theta)**2 + 6.9407766226753e+18)*cos(14*phi)

#@torch.jit.script
def Yl26_m15(theta, phi):
    return 3.17257134412823e-21*(1.0 - cos(theta)**2)**7.5*(7.46609927084163e+25*cos(theta)**11 - 8.05167568424097e+25*cos(theta)**9 + 2.95775841461913e+25*cos(theta)**7 - 4.40517210687956e+24*cos(theta)**5 + 2.44731783715531e+23*cos(theta)**3 - 3.41486209835625e+21*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl26_m16(theta, phi):
    return 1.47601377103699e-22*(1.0 - cos(theta)**2)**8*(8.21270919792579e+26*cos(theta)**10 - 7.24650811581687e+26*cos(theta)**8 + 2.07043089023339e+26*cos(theta)**6 - 2.20258605343978e+25*cos(theta)**4 + 7.34195351146593e+23*cos(theta)**2 - 3.41486209835625e+21)*cos(16*phi)

#@torch.jit.script
def Yl26_m17(theta, phi):
    return 7.11797046507269e-24*(1.0 - cos(theta)**2)**8.5*(8.21270919792579e+27*cos(theta)**9 - 5.7972064926535e+27*cos(theta)**7 + 1.24225853414004e+27*cos(theta)**5 - 8.81034421375912e+25*cos(theta)**3 + 1.46839070229319e+24*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl26_m18(theta, phi):
    return 3.57691474264813e-25*(1.0 - cos(theta)**2)**9*(7.39143827813321e+28*cos(theta)**8 - 4.05804454485745e+28*cos(theta)**6 + 6.21129267070018e+27*cos(theta)**4 - 2.64310326412774e+26*cos(theta)**2 + 1.46839070229319e+24)*cos(18*phi)

#@torch.jit.script
def Yl26_m19(theta, phi):
    return 1.88519959716718e-26*(1.0 - cos(theta)**2)**9.5*(5.91315062250657e+29*cos(theta)**7 - 2.43482672691447e+29*cos(theta)**5 + 2.48451706828007e+28*cos(theta)**3 - 5.28620652825547e+26*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl26_m20(theta, phi):
    return 1.0505806618571e-27*(1.0 - cos(theta)**2)**10*(4.1392054357546e+30*cos(theta)**6 - 1.21741336345723e+30*cos(theta)**4 + 7.45355120484021e+28*cos(theta)**2 - 5.28620652825547e+26)*cos(20*phi)

#@torch.jit.script
def Yl26_m21(theta, phi):
    return 6.25611679988175e-29*(1.0 - cos(theta)**2)**10.5*(2.48352326145276e+31*cos(theta)**5 - 4.86965345382894e+30*cos(theta)**3 + 1.49071024096804e+29*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl26_m22(theta, phi):
    return 4.03830602964508e-30*(1.0 - cos(theta)**2)**11*(1.24176163072638e+32*cos(theta)**4 - 1.46089603614868e+31*cos(theta)**2 + 1.49071024096804e+29)*cos(22*phi)

#@torch.jit.script
def Yl26_m23(theta, phi):
    return 2.88450430688934e-31*(1.0 - cos(theta)**2)**11.5*(4.96704652290552e+32*cos(theta)**3 - 2.92179207229736e+31*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl26_m24(theta, phi):
    return 2.35518790424645e-32*(1.0 - cos(theta)**2)**12*(1.49011395687166e+33*cos(theta)**2 - 2.92179207229736e+31)*cos(24*phi)

#@torch.jit.script
def Yl26_m25(theta, phi):
    return 6.94984237067387*(1.0 - cos(theta)**2)**12.5*cos(25*phi)*cos(theta)

#@torch.jit.script
def Yl26_m26(theta, phi):
    return 0.963769731686801*(1.0 - cos(theta)**2)**13*cos(26*phi)

#@torch.jit.script
def Yl27_m_minus_27(theta, phi):
    return 0.97265258980333*(1.0 - cos(theta)**2)**13.5*sin(27*phi)

#@torch.jit.script
def Yl27_m_minus_26(theta, phi):
    return 7.14750762604425*(1.0 - cos(theta)**2)**13*sin(26*phi)*cos(theta)

#@torch.jit.script
def Yl27_m_minus_25(theta, phi):
    return 4.65888737989014e-34*(1.0 - cos(theta)**2)**12.5*(7.89760397141977e+34*cos(theta)**2 - 1.49011395687166e+33)*sin(25*phi)

#@torch.jit.script
def Yl27_m_minus_24(theta, phi):
    return 5.81894847243549e-33*(1.0 - cos(theta)**2)**12*(2.63253465713992e+34*cos(theta)**3 - 1.49011395687166e+33*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl27_m_minus_23(theta, phi):
    return 8.31112080905536e-32*(1.0 - cos(theta)**2)**11.5*(6.58133664284981e+33*cos(theta)**4 - 7.45056978435828e+32*cos(theta)**2 + 7.30448018074341e+30)*sin(23*phi)

#@torch.jit.script
def Yl27_m_minus_22(theta, phi):
    return 1.31410358327182e-30*(1.0 - cos(theta)**2)**11*(1.31626732856996e+33*cos(theta)**5 - 2.48352326145276e+32*cos(theta)**3 + 7.30448018074341e+30*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl27_m_minus_21(theta, phi):
    return 2.25321827372525e-29*(1.0 - cos(theta)**2)**10.5*(2.19377888094994e+32*cos(theta)**6 - 6.2088081536319e+31*cos(theta)**4 + 3.6522400903717e+30*cos(theta)**2 - 2.48451706828007e+28)*sin(21*phi)

#@torch.jit.script
def Yl27_m_minus_20(theta, phi):
    return 4.13021731864148e-28*(1.0 - cos(theta)**2)**10*(3.13396982992848e+31*cos(theta)**7 - 1.24176163072638e+31*cos(theta)**5 + 1.21741336345723e+30*cos(theta)**3 - 2.48451706828007e+28*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl27_m_minus_19(theta, phi):
    return 8.00878852093215e-27*(1.0 - cos(theta)**2)**9.5*(3.9174622874106e+30*cos(theta)**8 - 2.0696027178773e+30*cos(theta)**6 + 3.04353340864309e+29*cos(theta)**4 - 1.24225853414004e+28*cos(theta)**2 + 6.60775816031934e+25)*sin(19*phi)

#@torch.jit.script
def Yl27_m_minus_18(theta, phi):
    return 1.62954739542083e-25*(1.0 - cos(theta)**2)**9*(4.35273587490067e+29*cos(theta)**9 - 2.95657531125328e+29*cos(theta)**7 + 6.08706681728617e+28*cos(theta)**5 - 4.14086178046679e+27*cos(theta)**3 + 6.60775816031934e+25*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl27_m_minus_17(theta, phi):
    return 3.45679204070083e-24*(1.0 - cos(theta)**2)**8.5*(4.35273587490067e+28*cos(theta)**10 - 3.69571913906661e+28*cos(theta)**8 + 1.01451113621436e+28*cos(theta)**6 - 1.0352154451167e+27*cos(theta)**4 + 3.30387908015967e+25*cos(theta)**2 - 1.46839070229319e+23)*sin(17*phi)

#@torch.jit.script
def Yl27_m_minus_16(theta, phi):
    return 7.60494248954183e-23*(1.0 - cos(theta)**2)**8*(3.95703261354606e+27*cos(theta)**11 - 4.1063545989629e+27*cos(theta)**9 + 1.44930162316337e+27*cos(theta)**7 - 2.07043089023339e+26*cos(theta)**5 + 1.10129302671989e+25*cos(theta)**3 - 1.46839070229319e+23*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl27_m_minus_15(theta, phi):
    return 1.72751085492761e-21*(1.0 - cos(theta)**2)**7.5*(3.29752717795505e+26*cos(theta)**12 - 4.1063545989629e+26*cos(theta)**10 + 1.81162702895422e+26*cos(theta)**8 - 3.45071815038899e+25*cos(theta)**6 + 2.75323256679972e+24*cos(theta)**4 - 7.34195351146593e+22*cos(theta)**2 + 2.84571841529687e+20)*sin(15*phi)

#@torch.jit.script
def Yl27_m_minus_14(theta, phi):
    return 4.03661292375851e-20*(1.0 - cos(theta)**2)**7*(2.53655936765773e+25*cos(theta)**13 - 3.73304963542081e+25*cos(theta)**11 + 2.01291892106024e+25*cos(theta)**9 - 4.92959735769855e+24*cos(theta)**7 + 5.50646513359945e+23*cos(theta)**5 - 2.44731783715531e+22*cos(theta)**3 + 2.84571841529687e+20*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl27_m_minus_13(theta, phi):
    return 9.67103717108456e-19*(1.0 - cos(theta)**2)**6.5*(1.81182811975552e+24*cos(theta)**14 - 3.11087469618401e+24*cos(theta)**12 + 2.01291892106024e+24*cos(theta)**10 - 6.16199669712319e+23*cos(theta)**8 + 9.17744188933241e+22*cos(theta)**6 - 6.11829459288828e+21*cos(theta)**4 + 1.42285920764844e+20*cos(theta)**2 - 4.95769758762521e+17)*sin(13*phi)

#@torch.jit.script
def Yl27_m_minus_12(theta, phi):
    return 2.36891063526465e-17*(1.0 - cos(theta)**2)**6*(1.20788541317035e+23*cos(theta)**15 - 2.39298053552616e+23*cos(theta)**13 + 1.82992629187295e+23*cos(theta)**11 - 6.84666299680355e+22*cos(theta)**9 + 1.31106312704749e+22*cos(theta)**7 - 1.22365891857766e+21*cos(theta)**5 + 4.74286402549479e+19*cos(theta)**3 - 4.95769758762521e+17*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl27_m_minus_11(theta, phi):
    return 5.91753687024496e-16*(1.0 - cos(theta)**2)**5.5*(7.54928383231468e+21*cos(theta)**16 - 1.70927181109012e+22*cos(theta)**14 + 1.52493857656079e+22*cos(theta)**12 - 6.84666299680355e+21*cos(theta)**10 + 1.63882890880936e+21*cos(theta)**8 - 2.03943153096276e+20*cos(theta)**6 + 1.1857160063737e+19*cos(theta)**4 - 2.47884879381261e+17*cos(theta)**2 + 794502818529682.0)*sin(11*phi)

#@torch.jit.script
def Yl27_m_minus_10(theta, phi):
    return 1.50403253709877e-14*(1.0 - cos(theta)**2)**5*(4.44075519547922e+20*cos(theta)**17 - 1.13951454072674e+21*cos(theta)**15 + 1.17302967427753e+21*cos(theta)**13 - 6.22423908800322e+20*cos(theta)**11 + 1.82092100978818e+20*cos(theta)**9 - 2.91347361566108e+19*cos(theta)**7 + 2.37143201274739e+18*cos(theta)**5 - 8.26282931270869e+16*cos(theta)**3 + 794502818529682.0*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl27_m_minus_9(theta, phi):
    return 3.8814531289017e-13*(1.0 - cos(theta)**2)**4.5*(2.46708621971068e+19*cos(theta)**18 - 7.12196587954215e+19*cos(theta)**16 + 8.37878338769665e+19*cos(theta)**14 - 5.18686590666935e+19*cos(theta)**12 + 1.82092100978818e+19*cos(theta)**10 - 3.64184201957635e+18*cos(theta)**8 + 3.95238668791232e+17*cos(theta)**6 - 2.06570732817717e+16*cos(theta)**4 + 397251409264841.0*cos(theta)**2 - 1192947174969.49)*sin(9*phi)

#@torch.jit.script
def Yl27_m_minus_8(theta, phi):
    return 1.01513171657834e-11*(1.0 - cos(theta)**2)**4*(1.29846643142667e+18*cos(theta)**19 - 4.18939169384832e+18*cos(theta)**17 + 5.58585559179777e+18*cos(theta)**15 - 3.98989685128412e+18*cos(theta)**13 + 1.65538273617107e+18*cos(theta)**11 - 4.04649113286262e+17*cos(theta)**9 + 5.6462666970176e+16*cos(theta)**7 - 4.13141465635434e+15*cos(theta)**5 + 132417136421614.0*cos(theta)**3 - 1192947174969.49*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl27_m_minus_7(theta, phi):
    return 2.68578607004038e-10*(1.0 - cos(theta)**2)**3.5*(6.49233215713337e+16*cos(theta)**20 - 2.32743982991574e+17*cos(theta)**18 + 3.4911597448736e+17*cos(theta)**16 - 2.8499263223458e+17*cos(theta)**14 + 1.37948561347589e+17*cos(theta)**12 - 4.04649113286262e+16*cos(theta)**10 + 7.05783337127201e+15*cos(theta)**8 - 688569109392391.0*cos(theta)**6 + 33104284105403.4*cos(theta)**4 - 596473587484.746*cos(theta)**2 + 1704210249.95642)*sin(7*phi)

#@torch.jit.script
def Yl27_m_minus_6(theta, phi):
    return 7.17662944926961e-9*(1.0 - cos(theta)**2)**3*(3.09158674149208e+15*cos(theta)**21 - 1.2249683315346e+16*cos(theta)**19 + 2.05362337933741e+16*cos(theta)**17 - 1.89995088156387e+16*cos(theta)**15 + 1.06114277959684e+16*cos(theta)**13 - 3.67862830260238e+15*cos(theta)**11 + 784203707919112.0*cos(theta)**9 - 98367015627484.4*cos(theta)**7 + 6620856821080.68*cos(theta)**5 - 198824529161.582*cos(theta)**3 + 1704210249.95642*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl27_m_minus_5(theta, phi):
    return 1.93369882461158e-7*(1.0 - cos(theta)**2)**2.5*(140526670067822.0*cos(theta)**22 - 612484165767299.0*cos(theta)**20 + 1.14090187740967e+15*cos(theta)**18 - 1.18746930097742e+15*cos(theta)**16 + 757959128283457.0*cos(theta)**14 - 306552358550198.0*cos(theta)**12 + 78420370791911.2*cos(theta)**10 - 12295876953435.5*cos(theta)**8 + 1103476136846.78*cos(theta)**6 - 49706132290.3955*cos(theta)**4 + 852105124.978209*cos(theta)**2 - 2347397.03850746)*sin(5*phi)

#@torch.jit.script
def Yl27_m_minus_4(theta, phi):
    return 5.24599340659887e-6*(1.0 - cos(theta)**2)**2*(6109855220340.08*cos(theta)**23 - 29165912655585.7*cos(theta)**21 + 60047467232088.1*cos(theta)**19 - 69851135351612.7*cos(theta)**17 + 50530608552230.5*cos(theta)**15 - 23580950657707.6*cos(theta)**13 + 7129124617446.47*cos(theta)**11 - 1366208550381.73*cos(theta)**9 + 157639448120.969*cos(theta)**7 - 9941226458.0791*cos(theta)**5 + 284035041.659403*cos(theta)**3 - 2347397.03850746*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl27_m_minus_3(theta, phi):
    return 0.00014309162252077*(1.0 - cos(theta)**2)**1.5*(254577300847.503*cos(theta)**24 - 1325723302526.62*cos(theta)**22 + 3002373361604.41*cos(theta)**20 - 3880618630645.15*cos(theta)**18 + 3158163034514.4*cos(theta)**16 - 1684353618407.68*cos(theta)**14 + 594093718120.539*cos(theta)**12 - 136620855038.173*cos(theta)**10 + 19704931015.1211*cos(theta)**8 - 1656871076.34652*cos(theta)**6 + 71008760.4148507*cos(theta)**4 - 1173698.51925373*cos(theta)**2 + 3155.103546381)*sin(3*phi)

#@torch.jit.script
def Yl27_m_minus_2(theta, phi):
    return 0.00391872547223201*(1.0 - cos(theta)**2)*(10183092033.9001*cos(theta)**25 - 57640143588.114*cos(theta)**23 + 142970160076.4*cos(theta)**21 - 204243085823.429*cos(theta)**19 + 185774296147.906*cos(theta)**17 - 112290241227.179*cos(theta)**15 + 45699516778.503*cos(theta)**13 - 12420077730.743*cos(theta)**11 + 2189436779.4579*cos(theta)**9 - 236695868.049502*cos(theta)**7 + 14201752.0829701*cos(theta)**5 - 391232.839751244*cos(theta)**3 + 3155.103546381*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl27_m_minus_1(theta, phi):
    return 0.107604519572121*(1.0 - cos(theta)**2)**0.5*(391657385.919236*cos(theta)**26 - 2401672649.50475*cos(theta)**24 + 6498643639.83638*cos(theta)**22 - 10212154291.1714*cos(theta)**20 + 10320794230.4392*cos(theta)**18 - 7018140076.69868*cos(theta)**16 + 3264251198.4645*cos(theta)**14 - 1035006477.56191*cos(theta)**12 + 218943677.94579*cos(theta)**10 - 29586983.5061878*cos(theta)**8 + 2366958.68049502*cos(theta)**6 - 97808.2099378109*cos(theta)**4 + 1577.5517731905*cos(theta)**2 - 4.18448746204376)*sin(phi)

#@torch.jit.script
def Yl27_m0(theta, phi):
    return 95338615.7975749*cos(theta)**27 - 631393474.432996*cos(theta)**25 + 1857039630.68528*cos(theta)**23 - 3196129432.40392*cos(theta)**21 + 3570144578.74906*cos(theta)**19 - 2713309879.84929*cos(theta)**17 + 1430271874.64924*cos(theta)**15 - 523270198.042403*cos(theta)**13 + 130817549.510601*cos(theta)**11 - 21606502.1714206*cos(theta)**9 + 2222383.08048897*cos(theta)**7 - 128567.616226635*cos(theta)**5 + 3456.11871576975*cos(theta)**3 - 27.5022709477699*cos(theta)

#@torch.jit.script
def Yl27_m1(theta, phi):
    return 0.107604519572121*(1.0 - cos(theta)**2)**0.5*(391657385.919236*cos(theta)**26 - 2401672649.50475*cos(theta)**24 + 6498643639.83638*cos(theta)**22 - 10212154291.1714*cos(theta)**20 + 10320794230.4392*cos(theta)**18 - 7018140076.69868*cos(theta)**16 + 3264251198.4645*cos(theta)**14 - 1035006477.56191*cos(theta)**12 + 218943677.94579*cos(theta)**10 - 29586983.5061878*cos(theta)**8 + 2366958.68049502*cos(theta)**6 - 97808.2099378109*cos(theta)**4 + 1577.5517731905*cos(theta)**2 - 4.18448746204376)*cos(phi)

#@torch.jit.script
def Yl27_m2(theta, phi):
    return 0.00391872547223201*(1.0 - cos(theta)**2)*(10183092033.9001*cos(theta)**25 - 57640143588.114*cos(theta)**23 + 142970160076.4*cos(theta)**21 - 204243085823.429*cos(theta)**19 + 185774296147.906*cos(theta)**17 - 112290241227.179*cos(theta)**15 + 45699516778.503*cos(theta)**13 - 12420077730.743*cos(theta)**11 + 2189436779.4579*cos(theta)**9 - 236695868.049502*cos(theta)**7 + 14201752.0829701*cos(theta)**5 - 391232.839751244*cos(theta)**3 + 3155.103546381*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl27_m3(theta, phi):
    return 0.00014309162252077*(1.0 - cos(theta)**2)**1.5*(254577300847.503*cos(theta)**24 - 1325723302526.62*cos(theta)**22 + 3002373361604.41*cos(theta)**20 - 3880618630645.15*cos(theta)**18 + 3158163034514.4*cos(theta)**16 - 1684353618407.68*cos(theta)**14 + 594093718120.539*cos(theta)**12 - 136620855038.173*cos(theta)**10 + 19704931015.1211*cos(theta)**8 - 1656871076.34652*cos(theta)**6 + 71008760.4148507*cos(theta)**4 - 1173698.51925373*cos(theta)**2 + 3155.103546381)*cos(3*phi)

#@torch.jit.script
def Yl27_m4(theta, phi):
    return 5.24599340659887e-6*(1.0 - cos(theta)**2)**2*(6109855220340.08*cos(theta)**23 - 29165912655585.7*cos(theta)**21 + 60047467232088.1*cos(theta)**19 - 69851135351612.7*cos(theta)**17 + 50530608552230.5*cos(theta)**15 - 23580950657707.6*cos(theta)**13 + 7129124617446.47*cos(theta)**11 - 1366208550381.73*cos(theta)**9 + 157639448120.969*cos(theta)**7 - 9941226458.0791*cos(theta)**5 + 284035041.659403*cos(theta)**3 - 2347397.03850746*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl27_m5(theta, phi):
    return 1.93369882461158e-7*(1.0 - cos(theta)**2)**2.5*(140526670067822.0*cos(theta)**22 - 612484165767299.0*cos(theta)**20 + 1.14090187740967e+15*cos(theta)**18 - 1.18746930097742e+15*cos(theta)**16 + 757959128283457.0*cos(theta)**14 - 306552358550198.0*cos(theta)**12 + 78420370791911.2*cos(theta)**10 - 12295876953435.5*cos(theta)**8 + 1103476136846.78*cos(theta)**6 - 49706132290.3955*cos(theta)**4 + 852105124.978209*cos(theta)**2 - 2347397.03850746)*cos(5*phi)

#@torch.jit.script
def Yl27_m6(theta, phi):
    return 7.17662944926961e-9*(1.0 - cos(theta)**2)**3*(3.09158674149208e+15*cos(theta)**21 - 1.2249683315346e+16*cos(theta)**19 + 2.05362337933741e+16*cos(theta)**17 - 1.89995088156387e+16*cos(theta)**15 + 1.06114277959684e+16*cos(theta)**13 - 3.67862830260238e+15*cos(theta)**11 + 784203707919112.0*cos(theta)**9 - 98367015627484.4*cos(theta)**7 + 6620856821080.68*cos(theta)**5 - 198824529161.582*cos(theta)**3 + 1704210249.95642*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl27_m7(theta, phi):
    return 2.68578607004038e-10*(1.0 - cos(theta)**2)**3.5*(6.49233215713337e+16*cos(theta)**20 - 2.32743982991574e+17*cos(theta)**18 + 3.4911597448736e+17*cos(theta)**16 - 2.8499263223458e+17*cos(theta)**14 + 1.37948561347589e+17*cos(theta)**12 - 4.04649113286262e+16*cos(theta)**10 + 7.05783337127201e+15*cos(theta)**8 - 688569109392391.0*cos(theta)**6 + 33104284105403.4*cos(theta)**4 - 596473587484.746*cos(theta)**2 + 1704210249.95642)*cos(7*phi)

#@torch.jit.script
def Yl27_m8(theta, phi):
    return 1.01513171657834e-11*(1.0 - cos(theta)**2)**4*(1.29846643142667e+18*cos(theta)**19 - 4.18939169384832e+18*cos(theta)**17 + 5.58585559179777e+18*cos(theta)**15 - 3.98989685128412e+18*cos(theta)**13 + 1.65538273617107e+18*cos(theta)**11 - 4.04649113286262e+17*cos(theta)**9 + 5.6462666970176e+16*cos(theta)**7 - 4.13141465635434e+15*cos(theta)**5 + 132417136421614.0*cos(theta)**3 - 1192947174969.49*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl27_m9(theta, phi):
    return 3.8814531289017e-13*(1.0 - cos(theta)**2)**4.5*(2.46708621971068e+19*cos(theta)**18 - 7.12196587954215e+19*cos(theta)**16 + 8.37878338769665e+19*cos(theta)**14 - 5.18686590666935e+19*cos(theta)**12 + 1.82092100978818e+19*cos(theta)**10 - 3.64184201957635e+18*cos(theta)**8 + 3.95238668791232e+17*cos(theta)**6 - 2.06570732817717e+16*cos(theta)**4 + 397251409264841.0*cos(theta)**2 - 1192947174969.49)*cos(9*phi)

#@torch.jit.script
def Yl27_m10(theta, phi):
    return 1.50403253709877e-14*(1.0 - cos(theta)**2)**5*(4.44075519547922e+20*cos(theta)**17 - 1.13951454072674e+21*cos(theta)**15 + 1.17302967427753e+21*cos(theta)**13 - 6.22423908800322e+20*cos(theta)**11 + 1.82092100978818e+20*cos(theta)**9 - 2.91347361566108e+19*cos(theta)**7 + 2.37143201274739e+18*cos(theta)**5 - 8.26282931270869e+16*cos(theta)**3 + 794502818529682.0*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl27_m11(theta, phi):
    return 5.91753687024496e-16*(1.0 - cos(theta)**2)**5.5*(7.54928383231468e+21*cos(theta)**16 - 1.70927181109012e+22*cos(theta)**14 + 1.52493857656079e+22*cos(theta)**12 - 6.84666299680355e+21*cos(theta)**10 + 1.63882890880936e+21*cos(theta)**8 - 2.03943153096276e+20*cos(theta)**6 + 1.1857160063737e+19*cos(theta)**4 - 2.47884879381261e+17*cos(theta)**2 + 794502818529682.0)*cos(11*phi)

#@torch.jit.script
def Yl27_m12(theta, phi):
    return 2.36891063526465e-17*(1.0 - cos(theta)**2)**6*(1.20788541317035e+23*cos(theta)**15 - 2.39298053552616e+23*cos(theta)**13 + 1.82992629187295e+23*cos(theta)**11 - 6.84666299680355e+22*cos(theta)**9 + 1.31106312704749e+22*cos(theta)**7 - 1.22365891857766e+21*cos(theta)**5 + 4.74286402549479e+19*cos(theta)**3 - 4.95769758762521e+17*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl27_m13(theta, phi):
    return 9.67103717108456e-19*(1.0 - cos(theta)**2)**6.5*(1.81182811975552e+24*cos(theta)**14 - 3.11087469618401e+24*cos(theta)**12 + 2.01291892106024e+24*cos(theta)**10 - 6.16199669712319e+23*cos(theta)**8 + 9.17744188933241e+22*cos(theta)**6 - 6.11829459288828e+21*cos(theta)**4 + 1.42285920764844e+20*cos(theta)**2 - 4.95769758762521e+17)*cos(13*phi)

#@torch.jit.script
def Yl27_m14(theta, phi):
    return 4.03661292375851e-20*(1.0 - cos(theta)**2)**7*(2.53655936765773e+25*cos(theta)**13 - 3.73304963542081e+25*cos(theta)**11 + 2.01291892106024e+25*cos(theta)**9 - 4.92959735769855e+24*cos(theta)**7 + 5.50646513359945e+23*cos(theta)**5 - 2.44731783715531e+22*cos(theta)**3 + 2.84571841529687e+20*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl27_m15(theta, phi):
    return 1.72751085492761e-21*(1.0 - cos(theta)**2)**7.5*(3.29752717795505e+26*cos(theta)**12 - 4.1063545989629e+26*cos(theta)**10 + 1.81162702895422e+26*cos(theta)**8 - 3.45071815038899e+25*cos(theta)**6 + 2.75323256679972e+24*cos(theta)**4 - 7.34195351146593e+22*cos(theta)**2 + 2.84571841529687e+20)*cos(15*phi)

#@torch.jit.script
def Yl27_m16(theta, phi):
    return 7.60494248954183e-23*(1.0 - cos(theta)**2)**8*(3.95703261354606e+27*cos(theta)**11 - 4.1063545989629e+27*cos(theta)**9 + 1.44930162316337e+27*cos(theta)**7 - 2.07043089023339e+26*cos(theta)**5 + 1.10129302671989e+25*cos(theta)**3 - 1.46839070229319e+23*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl27_m17(theta, phi):
    return 3.45679204070083e-24*(1.0 - cos(theta)**2)**8.5*(4.35273587490067e+28*cos(theta)**10 - 3.69571913906661e+28*cos(theta)**8 + 1.01451113621436e+28*cos(theta)**6 - 1.0352154451167e+27*cos(theta)**4 + 3.30387908015967e+25*cos(theta)**2 - 1.46839070229319e+23)*cos(17*phi)

#@torch.jit.script
def Yl27_m18(theta, phi):
    return 1.62954739542083e-25*(1.0 - cos(theta)**2)**9*(4.35273587490067e+29*cos(theta)**9 - 2.95657531125328e+29*cos(theta)**7 + 6.08706681728617e+28*cos(theta)**5 - 4.14086178046679e+27*cos(theta)**3 + 6.60775816031934e+25*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl27_m19(theta, phi):
    return 8.00878852093215e-27*(1.0 - cos(theta)**2)**9.5*(3.9174622874106e+30*cos(theta)**8 - 2.0696027178773e+30*cos(theta)**6 + 3.04353340864309e+29*cos(theta)**4 - 1.24225853414004e+28*cos(theta)**2 + 6.60775816031934e+25)*cos(19*phi)

#@torch.jit.script
def Yl27_m20(theta, phi):
    return 4.13021731864148e-28*(1.0 - cos(theta)**2)**10*(3.13396982992848e+31*cos(theta)**7 - 1.24176163072638e+31*cos(theta)**5 + 1.21741336345723e+30*cos(theta)**3 - 2.48451706828007e+28*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl27_m21(theta, phi):
    return 2.25321827372525e-29*(1.0 - cos(theta)**2)**10.5*(2.19377888094994e+32*cos(theta)**6 - 6.2088081536319e+31*cos(theta)**4 + 3.6522400903717e+30*cos(theta)**2 - 2.48451706828007e+28)*cos(21*phi)

#@torch.jit.script
def Yl27_m22(theta, phi):
    return 1.31410358327182e-30*(1.0 - cos(theta)**2)**11*(1.31626732856996e+33*cos(theta)**5 - 2.48352326145276e+32*cos(theta)**3 + 7.30448018074341e+30*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl27_m23(theta, phi):
    return 8.31112080905536e-32*(1.0 - cos(theta)**2)**11.5*(6.58133664284981e+33*cos(theta)**4 - 7.45056978435828e+32*cos(theta)**2 + 7.30448018074341e+30)*cos(23*phi)

#@torch.jit.script
def Yl27_m24(theta, phi):
    return 5.81894847243549e-33*(1.0 - cos(theta)**2)**12*(2.63253465713992e+34*cos(theta)**3 - 1.49011395687166e+33*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl27_m25(theta, phi):
    return 4.65888737989014e-34*(1.0 - cos(theta)**2)**12.5*(7.89760397141977e+34*cos(theta)**2 - 1.49011395687166e+33)*cos(25*phi)

#@torch.jit.script
def Yl27_m26(theta, phi):
    return 7.14750762604425*(1.0 - cos(theta)**2)**13*cos(26*phi)*cos(theta)

#@torch.jit.script
def Yl27_m27(theta, phi):
    return 0.97265258980333*(1.0 - cos(theta)**2)**13.5*cos(27*phi)

#@torch.jit.script
def Yl28_m_minus_28(theta, phi):
    return 0.981298560633835*(1.0 - cos(theta)**2)**14*sin(28*phi)

#@torch.jit.script
def Yl28_m_minus_27(theta, phi):
    return 7.34336601605245*(1.0 - cos(theta)**2)**13.5*sin(27*phi)*cos(theta)

#@torch.jit.script
def Yl28_m_minus_26(theta, phi):
    return 8.86550503264189e-36*(1.0 - cos(theta)**2)**13*(4.34368218428088e+36*cos(theta)**2 - 7.89760397141977e+34)*sin(26*phi)

#@torch.jit.script
def Yl28_m_minus_25(theta, phi):
    return 1.12839457090042e-34*(1.0 - cos(theta)**2)**12.5*(1.44789406142696e+36*cos(theta)**3 - 7.89760397141977e+34*cos(theta))*sin(25*phi)

#@torch.jit.script
def Yl28_m_minus_24(theta, phi):
    return 1.64296729492452e-33*(1.0 - cos(theta)**2)**12*(3.6197351535674e+35*cos(theta)**4 - 3.94880198570989e+34*cos(theta)**2 + 3.72528489217914e+32)*sin(24*phi)

#@torch.jit.script
def Yl28_m_minus_23(theta, phi):
    return 2.64920516074126e-32*(1.0 - cos(theta)**2)**11.5*(7.23947030713479e+34*cos(theta)**5 - 1.31626732856996e+34*cos(theta)**3 + 3.72528489217914e+32*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl28_m_minus_22(theta, phi):
    return 4.63421635555746e-31*(1.0 - cos(theta)**2)**11*(1.20657838452247e+34*cos(theta)**6 - 3.29066832142491e+33*cos(theta)**4 + 1.86264244608957e+32*cos(theta)**2 - 1.21741336345723e+30)*sin(22*phi)

#@torch.jit.script
def Yl28_m_minus_21(theta, phi):
    return 8.66982492934009e-30*(1.0 - cos(theta)**2)**10.5*(1.72368340646067e+33*cos(theta)**7 - 6.58133664284981e+32*cos(theta)**5 + 6.2088081536319e+31*cos(theta)**3 - 1.21741336345723e+30*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl28_m_minus_20(theta, phi):
    return 1.71653775978624e-28*(1.0 - cos(theta)**2)**10*(2.15460425807583e+32*cos(theta)**8 - 1.09688944047497e+32*cos(theta)**6 + 1.55220203840797e+31*cos(theta)**4 - 6.08706681728617e+29*cos(theta)**2 + 3.10564633535009e+27)*sin(20*phi)

#@torch.jit.script
def Yl28_m_minus_19(theta, phi):
    return 3.56775673567227e-27*(1.0 - cos(theta)**2)**9.5*(2.39400473119537e+31*cos(theta)**9 - 1.56698491496424e+31*cos(theta)**7 + 3.10440407681595e+30*cos(theta)**5 - 2.02902227242872e+29*cos(theta)**3 + 3.10564633535009e+27*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl28_m_minus_18(theta, phi):
    return 7.73471228858538e-26*(1.0 - cos(theta)**2)**9*(2.39400473119537e+30*cos(theta)**10 - 1.9587311437053e+30*cos(theta)**8 + 5.17400679469325e+29*cos(theta)**6 - 5.07255568107181e+28*cos(theta)**4 + 1.55282316767504e+27*cos(theta)**2 - 6.60775816031934e+24)*sin(18*phi)

#@torch.jit.script
def Yl28_m_minus_17(theta, phi):
    return 1.7398805056302e-24*(1.0 - cos(theta)**2)**8.5*(2.17636793745033e+29*cos(theta)**11 - 2.17636793745033e+29*cos(theta)**9 + 7.39143827813321e+28*cos(theta)**7 - 1.01451113621436e+28*cos(theta)**5 + 5.17607722558348e+26*cos(theta)**3 - 6.60775816031934e+24*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl28_m_minus_16(theta, phi):
    return 4.04311693361802e-23*(1.0 - cos(theta)**2)**8*(1.81363994787528e+28*cos(theta)**12 - 2.17636793745033e+28*cos(theta)**10 + 9.23929784766651e+27*cos(theta)**8 - 1.6908518936906e+27*cos(theta)**6 + 1.29401930639587e+26*cos(theta)**4 - 3.30387908015967e+24*cos(theta)**2 + 1.22365891857766e+22)*sin(16*phi)

#@torch.jit.script
def Yl28_m_minus_15(theta, phi):
    return 9.66972930141058e-22*(1.0 - cos(theta)**2)**7.5*(1.39510765221175e+27*cos(theta)**13 - 1.97851630677303e+27*cos(theta)**11 + 1.02658864974072e+27*cos(theta)**9 - 2.41550270527229e+26*cos(theta)**7 + 2.58803861279174e+25*cos(theta)**5 - 1.10129302671989e+24*cos(theta)**3 + 1.22365891857766e+22*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl28_m_minus_14(theta, phi):
    return 2.3725346401488e-20*(1.0 - cos(theta)**2)**7*(9.96505465865538e+25*cos(theta)**14 - 1.64876358897753e+26*cos(theta)**12 + 1.02658864974072e+26*cos(theta)**10 - 3.01937838159036e+25*cos(theta)**8 + 4.31339768798623e+24*cos(theta)**6 - 2.75323256679972e+23*cos(theta)**4 + 6.11829459288828e+21*cos(theta)**2 - 2.03265601092634e+19)*sin(14*phi)

#@torch.jit.script
def Yl28_m_minus_13(theta, phi):
    return 5.95501468493973e-19*(1.0 - cos(theta)**2)**6.5*(6.64336977243692e+24*cos(theta)**15 - 1.26827968382887e+25*cos(theta)**13 + 9.33262408855204e+24*cos(theta)**11 - 3.35486486843374e+24*cos(theta)**9 + 6.16199669712319e+23*cos(theta)**7 - 5.50646513359945e+22*cos(theta)**5 + 2.03943153096276e+21*cos(theta)**3 - 2.03265601092634e+19*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl28_m_minus_12(theta, phi):
    return 1.52522795453625e-17*(1.0 - cos(theta)**2)**6*(4.15210610777307e+23*cos(theta)**16 - 9.05914059877762e+23*cos(theta)**14 + 7.77718674046003e+23*cos(theta)**12 - 3.35486486843374e+23*cos(theta)**10 + 7.70249587140399e+22*cos(theta)**8 - 9.17744188933241e+21*cos(theta)**6 + 5.0985788274069e+20*cos(theta)**4 - 1.01632800546317e+19*cos(theta)**2 + 3.09856099226576e+16)*sin(12*phi)

#@torch.jit.script
def Yl28_m_minus_11(theta, phi):
    return 3.977307899878e-16*(1.0 - cos(theta)**2)**5.5*(2.44241535751357e+22*cos(theta)**17 - 6.03942706585174e+22*cos(theta)**15 + 5.98245133881541e+22*cos(theta)**13 - 3.04987715312158e+22*cos(theta)**11 + 8.55832874600443e+21*cos(theta)**9 - 1.31106312704749e+21*cos(theta)**7 + 1.01971576548138e+20*cos(theta)**5 - 3.38776001821056e+18*cos(theta)**3 + 3.09856099226576e+16*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl28_m_minus_10(theta, phi):
    return 1.05379896790437e-14*(1.0 - cos(theta)**2)**5*(1.35689742084087e+21*cos(theta)**18 - 3.77464191615734e+21*cos(theta)**16 + 4.27317952772529e+21*cos(theta)**14 - 2.54156429426798e+21*cos(theta)**12 + 8.55832874600443e+20*cos(theta)**10 - 1.63882890880936e+20*cos(theta)**8 + 1.6995262758023e+19*cos(theta)**6 - 8.46940004552641e+17*cos(theta)**4 + 1.54928049613288e+16*cos(theta)**2 - 44139045473871.2)*sin(10*phi)

#@torch.jit.script
def Yl28_m_minus_9(theta, phi):
    return 2.83156390560776e-13*(1.0 - cos(theta)**2)**4.5*(7.1415653728467e+19*cos(theta)**19 - 2.22037759773961e+20*cos(theta)**17 + 2.84878635181686e+20*cos(theta)**15 - 1.95504945712922e+20*cos(theta)**13 + 7.78029886000403e+19*cos(theta)**11 - 1.82092100978818e+19*cos(theta)**9 + 2.42789467971757e+18*cos(theta)**7 - 1.69388000910528e+17*cos(theta)**5 + 5.16426832044293e+15*cos(theta)**3 - 44139045473871.2*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl28_m_minus_8(theta, phi):
    return 7.70268659114473e-12*(1.0 - cos(theta)**2)**4*(3.57078268642335e+18*cos(theta)**20 - 1.23354310985534e+19*cos(theta)**18 + 1.78049146988554e+19*cos(theta)**16 - 1.39646389794944e+19*cos(theta)**14 + 6.48358238333669e+18*cos(theta)**12 - 1.82092100978818e+18*cos(theta)**10 + 3.03486834964696e+17*cos(theta)**8 - 2.8231333485088e+16*cos(theta)**6 + 1.29106708011073e+15*cos(theta)**4 - 22069522736935.6*cos(theta)**2 + 59647358748.4746)*sin(8*phi)

#@torch.jit.script
def Yl28_m_minus_7(theta, phi):
    return 2.11788866150653e-10*(1.0 - cos(theta)**2)**3.5*(1.70037270782064e+17*cos(theta)**21 - 6.49233215713337e+17*cos(theta)**19 + 1.04734792346208e+18*cos(theta)**17 - 9.30975931966294e+17*cos(theta)**15 + 4.98737106410515e+17*cos(theta)**13 - 1.65538273617107e+17*cos(theta)**11 + 3.37207594405218e+16*cos(theta)**9 - 4.03304764072686e+15*cos(theta)**7 + 258213416022147.0*cos(theta)**5 - 7356507578978.53*cos(theta)**3 + 59647358748.4746*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl28_m_minus_6(theta, phi):
    return 5.8769025298657e-9*(1.0 - cos(theta)**2)**3*(7.7289668537302e+15*cos(theta)**22 - 3.24616607856668e+16*cos(theta)**20 + 5.81859957478934e+16*cos(theta)**18 - 5.81859957478934e+16*cos(theta)**16 + 3.56240790293225e+16*cos(theta)**14 - 1.37948561347589e+16*cos(theta)**12 + 3.37207594405218e+15*cos(theta)**10 - 504130955090858.0*cos(theta)**8 + 43035569337024.4*cos(theta)**6 - 1839126894744.63*cos(theta)**4 + 29823679374.2373*cos(theta)**2 - 77464102.2707462)*sin(6*phi)

#@torch.jit.script
def Yl28_m_minus_5(theta, phi):
    return 1.64343247431143e-7*(1.0 - cos(theta)**2)**2.5*(336042037118704.0*cos(theta)**23 - 1.54579337074604e+15*cos(theta)**21 + 3.06242082883649e+15*cos(theta)**19 - 3.42270563222902e+15*cos(theta)**17 + 2.37493860195483e+15*cos(theta)**15 - 1.06114277959684e+15*cos(theta)**13 + 306552358550198.0*cos(theta)**11 - 56014550565650.8*cos(theta)**9 + 6147938476717.77*cos(theta)**7 - 367825378948.927*cos(theta)**5 + 9941226458.0791*cos(theta)**3 - 77464102.2707462*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl28_m_minus_4(theta, phi):
    return 4.62502894662956e-6*(1.0 - cos(theta)**2)**2*(14001751546612.7*cos(theta)**24 - 70263335033910.9*cos(theta)**22 + 153121041441825.0*cos(theta)**20 - 190150312901612.0*cos(theta)**18 + 148433662622177.0*cos(theta)**16 - 75795912828345.7*cos(theta)**14 + 25546029879183.2*cos(theta)**12 - 5601455056565.08*cos(theta)**10 + 768492309589.722*cos(theta)**8 - 61304229824.8211*cos(theta)**6 + 2485306614.51977*cos(theta)**4 - 38732051.1353731*cos(theta)**2 + 97808.2099378109)*sin(4*phi)

#@torch.jit.script
def Yl28_m_minus_3(theta, phi):
    return 0.000130815573253833*(1.0 - cos(theta)**2)**1.5*(560070061864.507*cos(theta)**25 - 3054927610170.04*cos(theta)**23 + 7291478163896.42*cos(theta)**21 - 10007911205348.0*cos(theta)**19 + 8731391918951.59*cos(theta)**17 - 5053060855223.05*cos(theta)**15 + 1965079221475.63*cos(theta)**13 - 509223186960.462*cos(theta)**11 + 85388034398.858*cos(theta)**9 - 8757747117.83159*cos(theta)**7 + 497061322.903955*cos(theta)**5 - 12910683.711791*cos(theta)**3 + 97808.2099378109*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl28_m_minus_2(theta, phi):
    return 0.00371387232545999*(1.0 - cos(theta)**2)*(21541156225.558*cos(theta)**26 - 127288650423.752*cos(theta)**24 + 331430825631.655*cos(theta)**22 - 500395560267.401*cos(theta)**20 + 485077328830.644*cos(theta)**18 - 315816303451.44*cos(theta)**16 + 140362801533.974*cos(theta)**14 - 42435265580.0385*cos(theta)**12 + 8538803439.8858*cos(theta)**10 - 1094718389.72895*cos(theta)**8 + 82843553.8173258*cos(theta)**6 - 3227670.92794776*cos(theta)**4 + 48904.1049689054*cos(theta)**2 - 121.350136399269)*sin(2*phi)

#@torch.jit.script
def Yl28_m_minus_1(theta, phi):
    return 0.105698659387677*(1.0 - cos(theta)**2)**0.5*(797820600.946591*cos(theta)**27 - 5091546016.95007*cos(theta)**25 + 14410035897.0285*cos(theta)**23 - 23828360012.7334*cos(theta)**21 + 25530385727.9286*cos(theta)**19 - 18577429614.7906*cos(theta)**17 + 9357520102.2649*cos(theta)**15 - 3264251198.4645*cos(theta)**13 + 776254858.171436*cos(theta)**11 - 121635376.63655*cos(theta)**9 + 11834793.4024751*cos(theta)**7 - 645534.185589552*cos(theta)**5 + 16301.3683229685*cos(theta)**3 - 121.350136399269*cos(theta))*sin(phi)

#@torch.jit.script
def Yl28_m0(theta, phi):
    return 190646827.826863*cos(theta)**28 - 1310263653.06463*cos(theta)**26 + 4017317804.20758*cos(theta)**24 - 7246926235.04112*cos(theta)**22 + 8541020205.58418*cos(theta)**20 - 6905505698.13189*cos(theta)**18 + 3913119895.60807*cos(theta)**16 - 1560047798.91352*cos(theta)**14 + 432818139.332713*cos(theta)**12 - 81384607.3958948*cos(theta)**10 + 9898127.92652775*cos(theta)**8 - 719863.849202018*cos(theta)**6 + 27267.570045531*cos(theta)**4 - 405.968784796988*cos(theta)**2 + 0.999923115263516

#@torch.jit.script
def Yl28_m1(theta, phi):
    return 0.105698659387677*(1.0 - cos(theta)**2)**0.5*(797820600.946591*cos(theta)**27 - 5091546016.95007*cos(theta)**25 + 14410035897.0285*cos(theta)**23 - 23828360012.7334*cos(theta)**21 + 25530385727.9286*cos(theta)**19 - 18577429614.7906*cos(theta)**17 + 9357520102.2649*cos(theta)**15 - 3264251198.4645*cos(theta)**13 + 776254858.171436*cos(theta)**11 - 121635376.63655*cos(theta)**9 + 11834793.4024751*cos(theta)**7 - 645534.185589552*cos(theta)**5 + 16301.3683229685*cos(theta)**3 - 121.350136399269*cos(theta))*cos(phi)

#@torch.jit.script
def Yl28_m2(theta, phi):
    return 0.00371387232545999*(1.0 - cos(theta)**2)*(21541156225.558*cos(theta)**26 - 127288650423.752*cos(theta)**24 + 331430825631.655*cos(theta)**22 - 500395560267.401*cos(theta)**20 + 485077328830.644*cos(theta)**18 - 315816303451.44*cos(theta)**16 + 140362801533.974*cos(theta)**14 - 42435265580.0385*cos(theta)**12 + 8538803439.8858*cos(theta)**10 - 1094718389.72895*cos(theta)**8 + 82843553.8173258*cos(theta)**6 - 3227670.92794776*cos(theta)**4 + 48904.1049689054*cos(theta)**2 - 121.350136399269)*cos(2*phi)

#@torch.jit.script
def Yl28_m3(theta, phi):
    return 0.000130815573253833*(1.0 - cos(theta)**2)**1.5*(560070061864.507*cos(theta)**25 - 3054927610170.04*cos(theta)**23 + 7291478163896.42*cos(theta)**21 - 10007911205348.0*cos(theta)**19 + 8731391918951.59*cos(theta)**17 - 5053060855223.05*cos(theta)**15 + 1965079221475.63*cos(theta)**13 - 509223186960.462*cos(theta)**11 + 85388034398.858*cos(theta)**9 - 8757747117.83159*cos(theta)**7 + 497061322.903955*cos(theta)**5 - 12910683.711791*cos(theta)**3 + 97808.2099378109*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl28_m4(theta, phi):
    return 4.62502894662956e-6*(1.0 - cos(theta)**2)**2*(14001751546612.7*cos(theta)**24 - 70263335033910.9*cos(theta)**22 + 153121041441825.0*cos(theta)**20 - 190150312901612.0*cos(theta)**18 + 148433662622177.0*cos(theta)**16 - 75795912828345.7*cos(theta)**14 + 25546029879183.2*cos(theta)**12 - 5601455056565.08*cos(theta)**10 + 768492309589.722*cos(theta)**8 - 61304229824.8211*cos(theta)**6 + 2485306614.51977*cos(theta)**4 - 38732051.1353731*cos(theta)**2 + 97808.2099378109)*cos(4*phi)

#@torch.jit.script
def Yl28_m5(theta, phi):
    return 1.64343247431143e-7*(1.0 - cos(theta)**2)**2.5*(336042037118704.0*cos(theta)**23 - 1.54579337074604e+15*cos(theta)**21 + 3.06242082883649e+15*cos(theta)**19 - 3.42270563222902e+15*cos(theta)**17 + 2.37493860195483e+15*cos(theta)**15 - 1.06114277959684e+15*cos(theta)**13 + 306552358550198.0*cos(theta)**11 - 56014550565650.8*cos(theta)**9 + 6147938476717.77*cos(theta)**7 - 367825378948.927*cos(theta)**5 + 9941226458.0791*cos(theta)**3 - 77464102.2707462*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl28_m6(theta, phi):
    return 5.8769025298657e-9*(1.0 - cos(theta)**2)**3*(7.7289668537302e+15*cos(theta)**22 - 3.24616607856668e+16*cos(theta)**20 + 5.81859957478934e+16*cos(theta)**18 - 5.81859957478934e+16*cos(theta)**16 + 3.56240790293225e+16*cos(theta)**14 - 1.37948561347589e+16*cos(theta)**12 + 3.37207594405218e+15*cos(theta)**10 - 504130955090858.0*cos(theta)**8 + 43035569337024.4*cos(theta)**6 - 1839126894744.63*cos(theta)**4 + 29823679374.2373*cos(theta)**2 - 77464102.2707462)*cos(6*phi)

#@torch.jit.script
def Yl28_m7(theta, phi):
    return 2.11788866150653e-10*(1.0 - cos(theta)**2)**3.5*(1.70037270782064e+17*cos(theta)**21 - 6.49233215713337e+17*cos(theta)**19 + 1.04734792346208e+18*cos(theta)**17 - 9.30975931966294e+17*cos(theta)**15 + 4.98737106410515e+17*cos(theta)**13 - 1.65538273617107e+17*cos(theta)**11 + 3.37207594405218e+16*cos(theta)**9 - 4.03304764072686e+15*cos(theta)**7 + 258213416022147.0*cos(theta)**5 - 7356507578978.53*cos(theta)**3 + 59647358748.4746*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl28_m8(theta, phi):
    return 7.70268659114473e-12*(1.0 - cos(theta)**2)**4*(3.57078268642335e+18*cos(theta)**20 - 1.23354310985534e+19*cos(theta)**18 + 1.78049146988554e+19*cos(theta)**16 - 1.39646389794944e+19*cos(theta)**14 + 6.48358238333669e+18*cos(theta)**12 - 1.82092100978818e+18*cos(theta)**10 + 3.03486834964696e+17*cos(theta)**8 - 2.8231333485088e+16*cos(theta)**6 + 1.29106708011073e+15*cos(theta)**4 - 22069522736935.6*cos(theta)**2 + 59647358748.4746)*cos(8*phi)

#@torch.jit.script
def Yl28_m9(theta, phi):
    return 2.83156390560776e-13*(1.0 - cos(theta)**2)**4.5*(7.1415653728467e+19*cos(theta)**19 - 2.22037759773961e+20*cos(theta)**17 + 2.84878635181686e+20*cos(theta)**15 - 1.95504945712922e+20*cos(theta)**13 + 7.78029886000403e+19*cos(theta)**11 - 1.82092100978818e+19*cos(theta)**9 + 2.42789467971757e+18*cos(theta)**7 - 1.69388000910528e+17*cos(theta)**5 + 5.16426832044293e+15*cos(theta)**3 - 44139045473871.2*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl28_m10(theta, phi):
    return 1.05379896790437e-14*(1.0 - cos(theta)**2)**5*(1.35689742084087e+21*cos(theta)**18 - 3.77464191615734e+21*cos(theta)**16 + 4.27317952772529e+21*cos(theta)**14 - 2.54156429426798e+21*cos(theta)**12 + 8.55832874600443e+20*cos(theta)**10 - 1.63882890880936e+20*cos(theta)**8 + 1.6995262758023e+19*cos(theta)**6 - 8.46940004552641e+17*cos(theta)**4 + 1.54928049613288e+16*cos(theta)**2 - 44139045473871.2)*cos(10*phi)

#@torch.jit.script
def Yl28_m11(theta, phi):
    return 3.977307899878e-16*(1.0 - cos(theta)**2)**5.5*(2.44241535751357e+22*cos(theta)**17 - 6.03942706585174e+22*cos(theta)**15 + 5.98245133881541e+22*cos(theta)**13 - 3.04987715312158e+22*cos(theta)**11 + 8.55832874600443e+21*cos(theta)**9 - 1.31106312704749e+21*cos(theta)**7 + 1.01971576548138e+20*cos(theta)**5 - 3.38776001821056e+18*cos(theta)**3 + 3.09856099226576e+16*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl28_m12(theta, phi):
    return 1.52522795453625e-17*(1.0 - cos(theta)**2)**6*(4.15210610777307e+23*cos(theta)**16 - 9.05914059877762e+23*cos(theta)**14 + 7.77718674046003e+23*cos(theta)**12 - 3.35486486843374e+23*cos(theta)**10 + 7.70249587140399e+22*cos(theta)**8 - 9.17744188933241e+21*cos(theta)**6 + 5.0985788274069e+20*cos(theta)**4 - 1.01632800546317e+19*cos(theta)**2 + 3.09856099226576e+16)*cos(12*phi)

#@torch.jit.script
def Yl28_m13(theta, phi):
    return 5.95501468493973e-19*(1.0 - cos(theta)**2)**6.5*(6.64336977243692e+24*cos(theta)**15 - 1.26827968382887e+25*cos(theta)**13 + 9.33262408855204e+24*cos(theta)**11 - 3.35486486843374e+24*cos(theta)**9 + 6.16199669712319e+23*cos(theta)**7 - 5.50646513359945e+22*cos(theta)**5 + 2.03943153096276e+21*cos(theta)**3 - 2.03265601092634e+19*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl28_m14(theta, phi):
    return 2.3725346401488e-20*(1.0 - cos(theta)**2)**7*(9.96505465865538e+25*cos(theta)**14 - 1.64876358897753e+26*cos(theta)**12 + 1.02658864974072e+26*cos(theta)**10 - 3.01937838159036e+25*cos(theta)**8 + 4.31339768798623e+24*cos(theta)**6 - 2.75323256679972e+23*cos(theta)**4 + 6.11829459288828e+21*cos(theta)**2 - 2.03265601092634e+19)*cos(14*phi)

#@torch.jit.script
def Yl28_m15(theta, phi):
    return 9.66972930141058e-22*(1.0 - cos(theta)**2)**7.5*(1.39510765221175e+27*cos(theta)**13 - 1.97851630677303e+27*cos(theta)**11 + 1.02658864974072e+27*cos(theta)**9 - 2.41550270527229e+26*cos(theta)**7 + 2.58803861279174e+25*cos(theta)**5 - 1.10129302671989e+24*cos(theta)**3 + 1.22365891857766e+22*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl28_m16(theta, phi):
    return 4.04311693361802e-23*(1.0 - cos(theta)**2)**8*(1.81363994787528e+28*cos(theta)**12 - 2.17636793745033e+28*cos(theta)**10 + 9.23929784766651e+27*cos(theta)**8 - 1.6908518936906e+27*cos(theta)**6 + 1.29401930639587e+26*cos(theta)**4 - 3.30387908015967e+24*cos(theta)**2 + 1.22365891857766e+22)*cos(16*phi)

#@torch.jit.script
def Yl28_m17(theta, phi):
    return 1.7398805056302e-24*(1.0 - cos(theta)**2)**8.5*(2.17636793745033e+29*cos(theta)**11 - 2.17636793745033e+29*cos(theta)**9 + 7.39143827813321e+28*cos(theta)**7 - 1.01451113621436e+28*cos(theta)**5 + 5.17607722558348e+26*cos(theta)**3 - 6.60775816031934e+24*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl28_m18(theta, phi):
    return 7.73471228858538e-26*(1.0 - cos(theta)**2)**9*(2.39400473119537e+30*cos(theta)**10 - 1.9587311437053e+30*cos(theta)**8 + 5.17400679469325e+29*cos(theta)**6 - 5.07255568107181e+28*cos(theta)**4 + 1.55282316767504e+27*cos(theta)**2 - 6.60775816031934e+24)*cos(18*phi)

#@torch.jit.script
def Yl28_m19(theta, phi):
    return 3.56775673567227e-27*(1.0 - cos(theta)**2)**9.5*(2.39400473119537e+31*cos(theta)**9 - 1.56698491496424e+31*cos(theta)**7 + 3.10440407681595e+30*cos(theta)**5 - 2.02902227242872e+29*cos(theta)**3 + 3.10564633535009e+27*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl28_m20(theta, phi):
    return 1.71653775978624e-28*(1.0 - cos(theta)**2)**10*(2.15460425807583e+32*cos(theta)**8 - 1.09688944047497e+32*cos(theta)**6 + 1.55220203840797e+31*cos(theta)**4 - 6.08706681728617e+29*cos(theta)**2 + 3.10564633535009e+27)*cos(20*phi)

#@torch.jit.script
def Yl28_m21(theta, phi):
    return 8.66982492934009e-30*(1.0 - cos(theta)**2)**10.5*(1.72368340646067e+33*cos(theta)**7 - 6.58133664284981e+32*cos(theta)**5 + 6.2088081536319e+31*cos(theta)**3 - 1.21741336345723e+30*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl28_m22(theta, phi):
    return 4.63421635555746e-31*(1.0 - cos(theta)**2)**11*(1.20657838452247e+34*cos(theta)**6 - 3.29066832142491e+33*cos(theta)**4 + 1.86264244608957e+32*cos(theta)**2 - 1.21741336345723e+30)*cos(22*phi)

#@torch.jit.script
def Yl28_m23(theta, phi):
    return 2.64920516074126e-32*(1.0 - cos(theta)**2)**11.5*(7.23947030713479e+34*cos(theta)**5 - 1.31626732856996e+34*cos(theta)**3 + 3.72528489217914e+32*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl28_m24(theta, phi):
    return 1.64296729492452e-33*(1.0 - cos(theta)**2)**12*(3.6197351535674e+35*cos(theta)**4 - 3.94880198570989e+34*cos(theta)**2 + 3.72528489217914e+32)*cos(24*phi)

#@torch.jit.script
def Yl28_m25(theta, phi):
    return 1.12839457090042e-34*(1.0 - cos(theta)**2)**12.5*(1.44789406142696e+36*cos(theta)**3 - 7.89760397141977e+34*cos(theta))*cos(25*phi)

#@torch.jit.script
def Yl28_m26(theta, phi):
    return 8.86550503264189e-36*(1.0 - cos(theta)**2)**13*(4.34368218428088e+36*cos(theta)**2 - 7.89760397141977e+34)*cos(26*phi)

#@torch.jit.script
def Yl28_m27(theta, phi):
    return 7.34336601605245*(1.0 - cos(theta)**2)**13.5*cos(27*phi)*cos(theta)

#@torch.jit.script
def Yl28_m28(theta, phi):
    return 0.981298560633835*(1.0 - cos(theta)**2)**14*cos(28*phi)

#@torch.jit.script
def Yl29_m_minus_29(theta, phi):
    return 0.989721878741179*(1.0 - cos(theta)**2)**14.5*sin(29*phi)

#@torch.jit.script
def Yl29_m_minus_28(theta, phi):
    return 7.53749726640217*(1.0 - cos(theta)**2)**14*sin(28*phi)*cos(theta)

#@torch.jit.script
def Yl29_m_minus_27(theta, phi):
    return 1.62523699825355e-37*(1.0 - cos(theta)**2)**13.5*(2.4758988450401e+38*cos(theta)**2 - 4.34368218428088e+36)*sin(27*phi)

#@torch.jit.script
def Yl29_m_minus_26(theta, phi):
    return 2.106547911828e-36*(1.0 - cos(theta)**2)**13*(8.25299615013366e+37*cos(theta)**3 - 4.34368218428088e+36*cos(theta))*sin(26*phi)

#@torch.jit.script
def Yl29_m_minus_25(theta, phi):
    return 3.12451548733867e-35*(1.0 - cos(theta)**2)**12.5*(2.06324903753342e+37*cos(theta)**4 - 2.17184109214044e+36*cos(theta)**2 + 1.97440099285494e+34)*sin(25*phi)

#@torch.jit.script
def Yl29_m_minus_24(theta, phi):
    return 5.13410284106891e-34*(1.0 - cos(theta)**2)**12*(4.12649807506683e+36*cos(theta)**5 - 7.23947030713479e+35*cos(theta)**3 + 1.97440099285494e+34*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl29_m_minus_23(theta, phi):
    return 9.15541687226183e-33*(1.0 - cos(theta)**2)**11.5*(6.87749679177805e+35*cos(theta)**6 - 1.8098675767837e+35*cos(theta)**4 + 9.87200496427472e+33*cos(theta)**2 - 6.2088081536319e+31)*sin(23*phi)

#@torch.jit.script
def Yl29_m_minus_22(theta, phi):
    return 1.74674221195294e-31*(1.0 - cos(theta)**2)**11*(9.82499541682579e+34*cos(theta)**7 - 3.6197351535674e+34*cos(theta)**5 + 3.29066832142491e+33*cos(theta)**3 - 6.2088081536319e+31*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl29_m_minus_21(theta, phi):
    return 3.52824631913283e-30*(1.0 - cos(theta)**2)**10.5*(1.22812442710322e+34*cos(theta)**8 - 6.03289192261233e+33*cos(theta)**6 + 8.22667080356226e+32*cos(theta)**4 - 3.10440407681595e+31*cos(theta)**2 + 1.52176670432154e+29)*sin(21*phi)

#@torch.jit.script
def Yl29_m_minus_20(theta, phi):
    return 7.48454069386591e-29*(1.0 - cos(theta)**2)**10*(1.36458269678136e+33*cos(theta)**9 - 8.61841703230333e+32*cos(theta)**7 + 1.64533416071245e+32*cos(theta)**5 - 1.03480135893865e+31*cos(theta)**3 + 1.52176670432154e+29*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl29_m_minus_19(theta, phi):
    return 1.65677370829833e-27*(1.0 - cos(theta)**2)**9.5*(1.36458269678136e+32*cos(theta)**10 - 1.07730212903792e+32*cos(theta)**8 + 2.74222360118742e+31*cos(theta)**6 - 2.58700339734662e+30*cos(theta)**4 + 7.60883352160772e+28*cos(theta)**2 - 3.10564633535009e+26)*sin(19*phi)

#@torch.jit.script
def Yl29_m_minus_18(theta, phi):
    return 3.80697614338276e-26*(1.0 - cos(theta)**2)**9*(1.24052972434669e+31*cos(theta)**11 - 1.19700236559768e+31*cos(theta)**9 + 3.9174622874106e+30*cos(theta)**7 - 5.17400679469325e+29*cos(theta)**5 + 2.53627784053591e+28*cos(theta)**3 - 3.10564633535009e+26*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl29_m_minus_17(theta, phi):
    return 9.04106740874383e-25*(1.0 - cos(theta)**2)**8.5*(1.03377477028891e+30*cos(theta)**12 - 1.19700236559768e+30*cos(theta)**10 + 4.89682785926325e+29*cos(theta)**8 - 8.62334465782208e+28*cos(theta)**6 + 6.34069460133976e+27*cos(theta)**4 - 1.55282316767504e+26*cos(theta)**2 + 5.50646513359945e+23)*sin(17*phi)

#@torch.jit.script
def Yl29_m_minus_16(theta, phi):
    return 2.21090610686865e-23*(1.0 - cos(theta)**2)**8*(7.95211361760699e+28*cos(theta)**13 - 1.08818396872517e+29*cos(theta)**11 + 5.44091984362584e+28*cos(theta)**9 - 1.23190637968887e+28*cos(theta)**7 + 1.26813892026795e+27*cos(theta)**5 - 5.17607722558348e+25*cos(theta)**3 + 5.50646513359945e+23*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl29_m_minus_15(theta, phi):
    return 5.54933028611123e-22*(1.0 - cos(theta)**2)**7.5*(5.68008115543357e+27*cos(theta)**14 - 9.06819973937639e+27*cos(theta)**12 + 5.44091984362584e+27*cos(theta)**10 - 1.53988297461109e+27*cos(theta)**8 + 2.11356486711325e+26*cos(theta)**6 - 1.29401930639587e+25*cos(theta)**4 + 2.75323256679972e+23*cos(theta)**2 - 8.74042084698325e+20)*sin(15*phi)

#@torch.jit.script
def Yl29_m_minus_14(theta, phi):
    return 1.42564876361858e-20*(1.0 - cos(theta)**2)**7*(3.78672077028904e+26*cos(theta)**15 - 6.97553826105876e+26*cos(theta)**13 + 4.94629076693258e+26*cos(theta)**11 - 1.71098108290121e+26*cos(theta)**9 + 3.01937838159036e+25*cos(theta)**7 - 2.58803861279174e+24*cos(theta)**5 + 9.17744188933241e+22*cos(theta)**3 - 8.74042084698325e+20*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl29_m_minus_13(theta, phi):
    return 3.7394416498704e-19*(1.0 - cos(theta)**2)**6.5*(2.36670048143065e+25*cos(theta)**16 - 4.98252732932769e+25*cos(theta)**14 + 4.12190897244381e+25*cos(theta)**12 - 1.71098108290121e+25*cos(theta)**10 + 3.77422297698796e+24*cos(theta)**8 - 4.31339768798623e+23*cos(theta)**6 + 2.2943604723331e+22*cos(theta)**4 - 4.37021042349163e+20*cos(theta)**2 + 1.27041000682896e+18)*sin(13*phi)

#@torch.jit.script
def Yl29_m_minus_12(theta, phi):
    return 9.99207917847372e-18*(1.0 - cos(theta)**2)**6*(1.39217675378274e+24*cos(theta)**17 - 3.32168488621846e+24*cos(theta)**15 + 3.17069920957217e+24*cos(theta)**13 - 1.55543734809201e+24*cos(theta)**11 + 4.19358108554217e+23*cos(theta)**9 - 6.16199669712319e+22*cos(theta)**7 + 4.58872094466621e+21*cos(theta)**5 - 1.45673680783054e+20*cos(theta)**3 + 1.27041000682896e+18*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl29_m_minus_11(theta, phi):
    return 2.7144637587553e-16*(1.0 - cos(theta)**2)**5.5*(7.73431529879298e+22*cos(theta)**18 - 2.07605305388654e+23*cos(theta)**16 + 2.2647851496944e+23*cos(theta)**14 - 1.29619779007667e+23*cos(theta)**12 + 4.19358108554217e+22*cos(theta)**10 - 7.70249587140399e+21*cos(theta)**8 + 7.64786824111034e+20*cos(theta)**6 - 3.64184201957635e+19*cos(theta)**4 + 6.35205003414481e+17*cos(theta)**2 - 1.72142277348098e+15)*sin(11*phi)

#@torch.jit.script
def Yl29_m_minus_10(theta, phi):
    return 7.48326015729302e-15*(1.0 - cos(theta)**2)**5*(4.07069226252262e+21*cos(theta)**19 - 1.22120767875679e+22*cos(theta)**17 + 1.50985676646294e+22*cos(theta)**15 - 9.97075223135901e+21*cos(theta)**13 + 3.81234644140198e+21*cos(theta)**11 - 8.55832874600443e+20*cos(theta)**9 + 1.09255260587291e+20*cos(theta)**7 - 7.28368403915271e+18*cos(theta)**5 + 2.1173500113816e+17*cos(theta)**3 - 1.72142277348098e+15*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl29_m_minus_9(theta, phi):
    return 2.08996082292824e-13*(1.0 - cos(theta)**2)**4.5*(2.03534613126131e+20*cos(theta)**20 - 6.78448710420437e+20*cos(theta)**18 + 9.43660479039335e+20*cos(theta)**16 - 7.12196587954215e+20*cos(theta)**14 + 3.17695536783498e+20*cos(theta)**12 - 8.55832874600443e+19*cos(theta)**10 + 1.36569075734113e+19*cos(theta)**8 - 1.21394733985879e+18*cos(theta)**6 + 5.293375028454e+16*cos(theta)**4 - 860711386740489.0*cos(theta)**2 + 2206952273693.56)*sin(9*phi)

#@torch.jit.script
def Yl29_m_minus_8(theta, phi):
    return 5.90390812988918e-12*(1.0 - cos(theta)**2)**4*(9.69212443457767e+18*cos(theta)**21 - 3.57078268642335e+19*cos(theta)**19 + 5.55094399434903e+19*cos(theta)**17 - 4.7479772530281e+19*cos(theta)**15 + 2.44381182141152e+19*cos(theta)**13 - 7.78029886000403e+18*cos(theta)**11 + 1.51743417482348e+18*cos(theta)**9 - 1.73421048551255e+17*cos(theta)**7 + 1.0586750056908e+16*cos(theta)**5 - 286903795580163.0*cos(theta)**3 + 2206952273693.56*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl29_m_minus_7(theta, phi):
    return 1.68442544512435e-10*(1.0 - cos(theta)**2)**3.5*(4.40551110662621e+17*cos(theta)**22 - 1.78539134321168e+18*cos(theta)**20 + 3.08385777463835e+18*cos(theta)**18 - 2.96748578314256e+18*cos(theta)**16 + 1.7455798724368e+18*cos(theta)**14 - 6.48358238333669e+17*cos(theta)**12 + 1.51743417482348e+17*cos(theta)**10 - 2.16776310689069e+16*cos(theta)**8 + 1.764458342818e+15*cos(theta)**6 - 71725948895040.7*cos(theta)**4 + 1103476136846.78*cos(theta)**2 - 2711243579.47612)*sin(7*phi)

#@torch.jit.script
def Yl29_m_minus_6(theta, phi):
    return 4.84693238903845e-9*(1.0 - cos(theta)**2)**3*(1.91543961157661e+16*cos(theta)**23 - 8.50186353910322e+16*cos(theta)**21 + 1.62308303928334e+17*cos(theta)**19 - 1.7455798724368e+17*cos(theta)**17 + 1.16371991495787e+17*cos(theta)**15 - 4.98737106410515e+16*cos(theta)**13 + 1.37948561347589e+16*cos(theta)**11 - 2.40862567432299e+15*cos(theta)**9 + 252065477545429.0*cos(theta)**7 - 14345189779008.1*cos(theta)**5 + 367825378948.927*cos(theta)**3 - 2711243579.47612*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl29_m_minus_5(theta, phi):
    return 1.40477446625728e-7*(1.0 - cos(theta)**2)**2.5*(798099838156923.0*cos(theta)**24 - 3.8644834268651e+15*cos(theta)**22 + 8.11541519641671e+15*cos(theta)**20 - 9.69766595798223e+15*cos(theta)**18 + 7.27324946848667e+15*cos(theta)**16 - 3.56240790293225e+15*cos(theta)**14 + 1.14957134456324e+15*cos(theta)**12 - 240862567432299.0*cos(theta)**10 + 31508184693178.6*cos(theta)**8 - 2390864963168.02*cos(theta)**6 + 91956344737.2317*cos(theta)**4 - 1355621789.73806*cos(theta)**2 + 3227670.92794776)*sin(5*phi)

#@torch.jit.script
def Yl29_m_minus_4(theta, phi):
    return 4.0955861679266e-6*(1.0 - cos(theta)**2)**2*(31923993526276.9*cos(theta)**25 - 168021018559352.0*cos(theta)**23 + 386448342686510.0*cos(theta)**21 - 510403471472749.0*cos(theta)**19 + 427838204028628.0*cos(theta)**17 - 237493860195483.0*cos(theta)**15 + 88428564966403.3*cos(theta)**13 - 21896597039299.9*cos(theta)**11 + 3500909410353.18*cos(theta)**9 - 341552137595.432*cos(theta)**7 + 18391268947.4463*cos(theta)**5 - 451873929.912686*cos(theta)**3 + 3227670.92794776*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl29_m_minus_3(theta, phi):
    return 0.000119966423463177*(1.0 - cos(theta)**2)**1.5*(1227845904856.8*cos(theta)**26 - 7000875773306.34*cos(theta)**24 + 17565833758477.7*cos(theta)**22 - 25520173573637.5*cos(theta)**20 + 23768789112701.5*cos(theta)**18 - 14843366262217.7*cos(theta)**16 + 6316326069028.81*cos(theta)**14 - 1824716419941.66*cos(theta)**12 + 350090941035.318*cos(theta)**10 - 42694017199.429*cos(theta)**8 + 3065211491.24106*cos(theta)**6 - 112968482.478172*cos(theta)**4 + 1613835.46397388*cos(theta)**2 - 3761.85422837734)*sin(3*phi)

#@torch.jit.script
def Yl29_m_minus_2(theta, phi):
    return 0.00352627828501722*(1.0 - cos(theta)**2)*(45475774253.9557*cos(theta)**27 - 280035030932.254*cos(theta)**25 + 763731902542.51*cos(theta)**23 - 1215246360649.4*cos(theta)**21 + 1250988900668.5*cos(theta)**19 - 873139191895.159*cos(theta)**17 + 421088404601.921*cos(theta)**15 - 140362801533.974*cos(theta)**13 + 31826449185.0289*cos(theta)**11 - 4743779688.82544*cos(theta)**9 + 437887355.891579*cos(theta)**7 - 22593696.4956343*cos(theta)**5 + 537945.15465796*cos(theta)**3 - 3761.85422837734*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl29_m_minus_1(theta, phi):
    return 0.103890645660027*(1.0 - cos(theta)**2)**0.5*(1624134794.78413*cos(theta)**28 - 10770578112.779*cos(theta)**26 + 31822162605.9379*cos(theta)**24 - 55238470938.6092*cos(theta)**22 + 62549445033.4251*cos(theta)**20 - 48507732883.0644*cos(theta)**18 + 26318025287.62*cos(theta)**16 - 10025914395.2838*cos(theta)**14 + 2652204098.75241*cos(theta)**12 - 474377968.882544*cos(theta)**10 + 54735919.4864474*cos(theta)**8 - 3765616.08260572*cos(theta)**6 + 134486.28866449*cos(theta)**4 - 1880.92711418867*cos(theta)**2 + 4.33393344283104)*sin(phi)

#@torch.jit.script
def Yl29_m0(theta, phi):
    return 381236978.781522*cos(theta)**29 - 2715477427.81224*cos(theta)**27 + 8664841610.56452*cos(theta)**25 - 16348757755.7821*cos(theta)**23 + 20275665255.9455*cos(theta)**21 - 17379141647.9533*cos(theta)**19 + 10538415680.1419*cos(theta)**17 - 4549919150.79141*cos(theta)**15 + 1388783461.72412*cos(theta)**13 - 293563983.779083*cos(theta)**11 + 41400048.994486*cos(theta)**9 - 3661920.79558107*cos(theta)**7 + 183096.039779054*cos(theta)**5 - 4267.9729552227*cos(theta)**3 + 29.5021172020002*cos(theta)

#@torch.jit.script
def Yl29_m1(theta, phi):
    return 0.103890645660027*(1.0 - cos(theta)**2)**0.5*(1624134794.78413*cos(theta)**28 - 10770578112.779*cos(theta)**26 + 31822162605.9379*cos(theta)**24 - 55238470938.6092*cos(theta)**22 + 62549445033.4251*cos(theta)**20 - 48507732883.0644*cos(theta)**18 + 26318025287.62*cos(theta)**16 - 10025914395.2838*cos(theta)**14 + 2652204098.75241*cos(theta)**12 - 474377968.882544*cos(theta)**10 + 54735919.4864474*cos(theta)**8 - 3765616.08260572*cos(theta)**6 + 134486.28866449*cos(theta)**4 - 1880.92711418867*cos(theta)**2 + 4.33393344283104)*cos(phi)

#@torch.jit.script
def Yl29_m2(theta, phi):
    return 0.00352627828501722*(1.0 - cos(theta)**2)*(45475774253.9557*cos(theta)**27 - 280035030932.254*cos(theta)**25 + 763731902542.51*cos(theta)**23 - 1215246360649.4*cos(theta)**21 + 1250988900668.5*cos(theta)**19 - 873139191895.159*cos(theta)**17 + 421088404601.921*cos(theta)**15 - 140362801533.974*cos(theta)**13 + 31826449185.0289*cos(theta)**11 - 4743779688.82544*cos(theta)**9 + 437887355.891579*cos(theta)**7 - 22593696.4956343*cos(theta)**5 + 537945.15465796*cos(theta)**3 - 3761.85422837734*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl29_m3(theta, phi):
    return 0.000119966423463177*(1.0 - cos(theta)**2)**1.5*(1227845904856.8*cos(theta)**26 - 7000875773306.34*cos(theta)**24 + 17565833758477.7*cos(theta)**22 - 25520173573637.5*cos(theta)**20 + 23768789112701.5*cos(theta)**18 - 14843366262217.7*cos(theta)**16 + 6316326069028.81*cos(theta)**14 - 1824716419941.66*cos(theta)**12 + 350090941035.318*cos(theta)**10 - 42694017199.429*cos(theta)**8 + 3065211491.24106*cos(theta)**6 - 112968482.478172*cos(theta)**4 + 1613835.46397388*cos(theta)**2 - 3761.85422837734)*cos(3*phi)

#@torch.jit.script
def Yl29_m4(theta, phi):
    return 4.0955861679266e-6*(1.0 - cos(theta)**2)**2*(31923993526276.9*cos(theta)**25 - 168021018559352.0*cos(theta)**23 + 386448342686510.0*cos(theta)**21 - 510403471472749.0*cos(theta)**19 + 427838204028628.0*cos(theta)**17 - 237493860195483.0*cos(theta)**15 + 88428564966403.3*cos(theta)**13 - 21896597039299.9*cos(theta)**11 + 3500909410353.18*cos(theta)**9 - 341552137595.432*cos(theta)**7 + 18391268947.4463*cos(theta)**5 - 451873929.912686*cos(theta)**3 + 3227670.92794776*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl29_m5(theta, phi):
    return 1.40477446625728e-7*(1.0 - cos(theta)**2)**2.5*(798099838156923.0*cos(theta)**24 - 3.8644834268651e+15*cos(theta)**22 + 8.11541519641671e+15*cos(theta)**20 - 9.69766595798223e+15*cos(theta)**18 + 7.27324946848667e+15*cos(theta)**16 - 3.56240790293225e+15*cos(theta)**14 + 1.14957134456324e+15*cos(theta)**12 - 240862567432299.0*cos(theta)**10 + 31508184693178.6*cos(theta)**8 - 2390864963168.02*cos(theta)**6 + 91956344737.2317*cos(theta)**4 - 1355621789.73806*cos(theta)**2 + 3227670.92794776)*cos(5*phi)

#@torch.jit.script
def Yl29_m6(theta, phi):
    return 4.84693238903845e-9*(1.0 - cos(theta)**2)**3*(1.91543961157661e+16*cos(theta)**23 - 8.50186353910322e+16*cos(theta)**21 + 1.62308303928334e+17*cos(theta)**19 - 1.7455798724368e+17*cos(theta)**17 + 1.16371991495787e+17*cos(theta)**15 - 4.98737106410515e+16*cos(theta)**13 + 1.37948561347589e+16*cos(theta)**11 - 2.40862567432299e+15*cos(theta)**9 + 252065477545429.0*cos(theta)**7 - 14345189779008.1*cos(theta)**5 + 367825378948.927*cos(theta)**3 - 2711243579.47612*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl29_m7(theta, phi):
    return 1.68442544512435e-10*(1.0 - cos(theta)**2)**3.5*(4.40551110662621e+17*cos(theta)**22 - 1.78539134321168e+18*cos(theta)**20 + 3.08385777463835e+18*cos(theta)**18 - 2.96748578314256e+18*cos(theta)**16 + 1.7455798724368e+18*cos(theta)**14 - 6.48358238333669e+17*cos(theta)**12 + 1.51743417482348e+17*cos(theta)**10 - 2.16776310689069e+16*cos(theta)**8 + 1.764458342818e+15*cos(theta)**6 - 71725948895040.7*cos(theta)**4 + 1103476136846.78*cos(theta)**2 - 2711243579.47612)*cos(7*phi)

#@torch.jit.script
def Yl29_m8(theta, phi):
    return 5.90390812988918e-12*(1.0 - cos(theta)**2)**4*(9.69212443457767e+18*cos(theta)**21 - 3.57078268642335e+19*cos(theta)**19 + 5.55094399434903e+19*cos(theta)**17 - 4.7479772530281e+19*cos(theta)**15 + 2.44381182141152e+19*cos(theta)**13 - 7.78029886000403e+18*cos(theta)**11 + 1.51743417482348e+18*cos(theta)**9 - 1.73421048551255e+17*cos(theta)**7 + 1.0586750056908e+16*cos(theta)**5 - 286903795580163.0*cos(theta)**3 + 2206952273693.56*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl29_m9(theta, phi):
    return 2.08996082292824e-13*(1.0 - cos(theta)**2)**4.5*(2.03534613126131e+20*cos(theta)**20 - 6.78448710420437e+20*cos(theta)**18 + 9.43660479039335e+20*cos(theta)**16 - 7.12196587954215e+20*cos(theta)**14 + 3.17695536783498e+20*cos(theta)**12 - 8.55832874600443e+19*cos(theta)**10 + 1.36569075734113e+19*cos(theta)**8 - 1.21394733985879e+18*cos(theta)**6 + 5.293375028454e+16*cos(theta)**4 - 860711386740489.0*cos(theta)**2 + 2206952273693.56)*cos(9*phi)

#@torch.jit.script
def Yl29_m10(theta, phi):
    return 7.48326015729302e-15*(1.0 - cos(theta)**2)**5*(4.07069226252262e+21*cos(theta)**19 - 1.22120767875679e+22*cos(theta)**17 + 1.50985676646294e+22*cos(theta)**15 - 9.97075223135901e+21*cos(theta)**13 + 3.81234644140198e+21*cos(theta)**11 - 8.55832874600443e+20*cos(theta)**9 + 1.09255260587291e+20*cos(theta)**7 - 7.28368403915271e+18*cos(theta)**5 + 2.1173500113816e+17*cos(theta)**3 - 1.72142277348098e+15*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl29_m11(theta, phi):
    return 2.7144637587553e-16*(1.0 - cos(theta)**2)**5.5*(7.73431529879298e+22*cos(theta)**18 - 2.07605305388654e+23*cos(theta)**16 + 2.2647851496944e+23*cos(theta)**14 - 1.29619779007667e+23*cos(theta)**12 + 4.19358108554217e+22*cos(theta)**10 - 7.70249587140399e+21*cos(theta)**8 + 7.64786824111034e+20*cos(theta)**6 - 3.64184201957635e+19*cos(theta)**4 + 6.35205003414481e+17*cos(theta)**2 - 1.72142277348098e+15)*cos(11*phi)

#@torch.jit.script
def Yl29_m12(theta, phi):
    return 9.99207917847372e-18*(1.0 - cos(theta)**2)**6*(1.39217675378274e+24*cos(theta)**17 - 3.32168488621846e+24*cos(theta)**15 + 3.17069920957217e+24*cos(theta)**13 - 1.55543734809201e+24*cos(theta)**11 + 4.19358108554217e+23*cos(theta)**9 - 6.16199669712319e+22*cos(theta)**7 + 4.58872094466621e+21*cos(theta)**5 - 1.45673680783054e+20*cos(theta)**3 + 1.27041000682896e+18*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl29_m13(theta, phi):
    return 3.7394416498704e-19*(1.0 - cos(theta)**2)**6.5*(2.36670048143065e+25*cos(theta)**16 - 4.98252732932769e+25*cos(theta)**14 + 4.12190897244381e+25*cos(theta)**12 - 1.71098108290121e+25*cos(theta)**10 + 3.77422297698796e+24*cos(theta)**8 - 4.31339768798623e+23*cos(theta)**6 + 2.2943604723331e+22*cos(theta)**4 - 4.37021042349163e+20*cos(theta)**2 + 1.27041000682896e+18)*cos(13*phi)

#@torch.jit.script
def Yl29_m14(theta, phi):
    return 1.42564876361858e-20*(1.0 - cos(theta)**2)**7*(3.78672077028904e+26*cos(theta)**15 - 6.97553826105876e+26*cos(theta)**13 + 4.94629076693258e+26*cos(theta)**11 - 1.71098108290121e+26*cos(theta)**9 + 3.01937838159036e+25*cos(theta)**7 - 2.58803861279174e+24*cos(theta)**5 + 9.17744188933241e+22*cos(theta)**3 - 8.74042084698325e+20*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl29_m15(theta, phi):
    return 5.54933028611123e-22*(1.0 - cos(theta)**2)**7.5*(5.68008115543357e+27*cos(theta)**14 - 9.06819973937639e+27*cos(theta)**12 + 5.44091984362584e+27*cos(theta)**10 - 1.53988297461109e+27*cos(theta)**8 + 2.11356486711325e+26*cos(theta)**6 - 1.29401930639587e+25*cos(theta)**4 + 2.75323256679972e+23*cos(theta)**2 - 8.74042084698325e+20)*cos(15*phi)

#@torch.jit.script
def Yl29_m16(theta, phi):
    return 2.21090610686865e-23*(1.0 - cos(theta)**2)**8*(7.95211361760699e+28*cos(theta)**13 - 1.08818396872517e+29*cos(theta)**11 + 5.44091984362584e+28*cos(theta)**9 - 1.23190637968887e+28*cos(theta)**7 + 1.26813892026795e+27*cos(theta)**5 - 5.17607722558348e+25*cos(theta)**3 + 5.50646513359945e+23*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl29_m17(theta, phi):
    return 9.04106740874383e-25*(1.0 - cos(theta)**2)**8.5*(1.03377477028891e+30*cos(theta)**12 - 1.19700236559768e+30*cos(theta)**10 + 4.89682785926325e+29*cos(theta)**8 - 8.62334465782208e+28*cos(theta)**6 + 6.34069460133976e+27*cos(theta)**4 - 1.55282316767504e+26*cos(theta)**2 + 5.50646513359945e+23)*cos(17*phi)

#@torch.jit.script
def Yl29_m18(theta, phi):
    return 3.80697614338276e-26*(1.0 - cos(theta)**2)**9*(1.24052972434669e+31*cos(theta)**11 - 1.19700236559768e+31*cos(theta)**9 + 3.9174622874106e+30*cos(theta)**7 - 5.17400679469325e+29*cos(theta)**5 + 2.53627784053591e+28*cos(theta)**3 - 3.10564633535009e+26*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl29_m19(theta, phi):
    return 1.65677370829833e-27*(1.0 - cos(theta)**2)**9.5*(1.36458269678136e+32*cos(theta)**10 - 1.07730212903792e+32*cos(theta)**8 + 2.74222360118742e+31*cos(theta)**6 - 2.58700339734662e+30*cos(theta)**4 + 7.60883352160772e+28*cos(theta)**2 - 3.10564633535009e+26)*cos(19*phi)

#@torch.jit.script
def Yl29_m20(theta, phi):
    return 7.48454069386591e-29*(1.0 - cos(theta)**2)**10*(1.36458269678136e+33*cos(theta)**9 - 8.61841703230333e+32*cos(theta)**7 + 1.64533416071245e+32*cos(theta)**5 - 1.03480135893865e+31*cos(theta)**3 + 1.52176670432154e+29*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl29_m21(theta, phi):
    return 3.52824631913283e-30*(1.0 - cos(theta)**2)**10.5*(1.22812442710322e+34*cos(theta)**8 - 6.03289192261233e+33*cos(theta)**6 + 8.22667080356226e+32*cos(theta)**4 - 3.10440407681595e+31*cos(theta)**2 + 1.52176670432154e+29)*cos(21*phi)

#@torch.jit.script
def Yl29_m22(theta, phi):
    return 1.74674221195294e-31*(1.0 - cos(theta)**2)**11*(9.82499541682579e+34*cos(theta)**7 - 3.6197351535674e+34*cos(theta)**5 + 3.29066832142491e+33*cos(theta)**3 - 6.2088081536319e+31*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl29_m23(theta, phi):
    return 9.15541687226183e-33*(1.0 - cos(theta)**2)**11.5*(6.87749679177805e+35*cos(theta)**6 - 1.8098675767837e+35*cos(theta)**4 + 9.87200496427472e+33*cos(theta)**2 - 6.2088081536319e+31)*cos(23*phi)

#@torch.jit.script
def Yl29_m24(theta, phi):
    return 5.13410284106891e-34*(1.0 - cos(theta)**2)**12*(4.12649807506683e+36*cos(theta)**5 - 7.23947030713479e+35*cos(theta)**3 + 1.97440099285494e+34*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl29_m25(theta, phi):
    return 3.12451548733867e-35*(1.0 - cos(theta)**2)**12.5*(2.06324903753342e+37*cos(theta)**4 - 2.17184109214044e+36*cos(theta)**2 + 1.97440099285494e+34)*cos(25*phi)

#@torch.jit.script
def Yl29_m26(theta, phi):
    return 2.106547911828e-36*(1.0 - cos(theta)**2)**13*(8.25299615013366e+37*cos(theta)**3 - 4.34368218428088e+36*cos(theta))*cos(26*phi)

#@torch.jit.script
def Yl29_m27(theta, phi):
    return 1.62523699825355e-37*(1.0 - cos(theta)**2)**13.5*(2.4758988450401e+38*cos(theta)**2 - 4.34368218428088e+36)*cos(27*phi)

#@torch.jit.script
def Yl29_m28(theta, phi):
    return 7.53749726640217*(1.0 - cos(theta)**2)**14*cos(28*phi)*cos(theta)

#@torch.jit.script
def Yl29_m29(theta, phi):
    return 0.989721878741179*(1.0 - cos(theta)**2)**14.5*cos(29*phi)

#@torch.jit.script
def Yl30_m_minus_30(theta, phi):
    return 0.997935479150139*(1.0 - cos(theta)**2)**15*sin(30*phi)

#@torch.jit.script
def Yl30_m_minus_29(theta, phi):
    return 7.72997498267602*(1.0 - cos(theta)**2)**14.5*sin(29*phi)*cos(theta)

#@torch.jit.script
def Yl30_m_minus_28(theta, phi):
    return 2.87411530575892e-39*(1.0 - cos(theta)**2)**14*(1.46078031857366e+40*cos(theta)**2 - 2.4758988450401e+38)*sin(28*phi)

#@torch.jit.script
def Yl30_m_minus_27(theta, phi):
    return 3.79121847114987e-38*(1.0 - cos(theta)**2)**13.5*(4.86926772857886e+39*cos(theta)**3 - 2.4758988450401e+38*cos(theta))*sin(27*phi)

#@torch.jit.script
def Yl30_m_minus_26(theta, phi):
    return 5.72461435302436e-37*(1.0 - cos(theta)**2)**13*(1.21731693214472e+39*cos(theta)**4 - 1.23794942252005e+38*cos(theta)**2 + 1.08592054607022e+36)*sin(26*phi)

#@torch.jit.script
def Yl30_m_minus_25(theta, phi):
    return 9.57911199299742e-36*(1.0 - cos(theta)**2)**12.5*(2.43463386428943e+38*cos(theta)**5 - 4.12649807506683e+37*cos(theta)**3 + 1.08592054607022e+36*cos(theta))*sin(25*phi)

#@torch.jit.script
def Yl30_m_minus_24(theta, phi):
    return 1.74013210905229e-34*(1.0 - cos(theta)**2)**12*(4.05772310714905e+37*cos(theta)**6 - 1.03162451876671e+37*cos(theta)**4 + 5.42960273035109e+35*cos(theta)**2 - 3.29066832142491e+33)*sin(24*phi)

#@torch.jit.script
def Yl30_m_minus_23(theta, phi):
    return 3.38320349392245e-33*(1.0 - cos(theta)**2)**11.5*(5.79674729592722e+36*cos(theta)**7 - 2.06324903753342e+36*cos(theta)**5 + 1.8098675767837e+35*cos(theta)**3 - 3.29066832142491e+33*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl30_m_minus_22(theta, phi):
    return 6.96644237302409e-32*(1.0 - cos(theta)**2)**11*(7.24593411990902e+35*cos(theta)**8 - 3.43874839588903e+35*cos(theta)**6 + 4.52466894195925e+34*cos(theta)**4 - 1.64533416071245e+33*cos(theta)**2 + 7.76101019203987e+30)*sin(22*phi)

#@torch.jit.script
def Yl30_m_minus_21(theta, phi):
    return 1.5070719110102e-30*(1.0 - cos(theta)**2)**10.5*(8.05103791101002e+34*cos(theta)**9 - 4.9124977084129e+34*cos(theta)**7 + 9.04933788391849e+33*cos(theta)**5 - 5.48444720237484e+32*cos(theta)**3 + 7.76101019203987e+30*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl30_m_minus_20(theta, phi):
    return 3.40344756082348e-29*(1.0 - cos(theta)**2)**10*(8.05103791101002e+33*cos(theta)**10 - 6.14062213551612e+33*cos(theta)**8 + 1.50822298065308e+33*cos(theta)**6 - 1.37111180059371e+32*cos(theta)**4 + 3.88050509601994e+30*cos(theta)**2 - 1.52176670432154e+28)*sin(20*phi)

#@torch.jit.script
def Yl30_m_minus_19(theta, phi):
    return 7.98179203850954e-28*(1.0 - cos(theta)**2)**9.5*(7.31912537364547e+32*cos(theta)**11 - 6.8229134839068e+32*cos(theta)**9 + 2.15460425807583e+32*cos(theta)**7 - 2.74222360118742e+31*cos(theta)**5 + 1.29350169867331e+30*cos(theta)**3 - 1.52176670432154e+28*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl30_m_minus_18(theta, phi):
    return 1.93548170846062e-26*(1.0 - cos(theta)**2)**9*(6.09927114470456e+31*cos(theta)**12 - 6.8229134839068e+31*cos(theta)**10 + 2.69325532259479e+31*cos(theta)**8 - 4.5703726686457e+30*cos(theta)**6 + 3.23375424668328e+29*cos(theta)**4 - 7.60883352160772e+27*cos(theta)**2 + 2.58803861279174e+25)*sin(18*phi)

#@torch.jit.script
def Yl30_m_minus_17(theta, phi):
    return 4.83483175810931e-25*(1.0 - cos(theta)**2)**8.5*(4.69174703438813e+30*cos(theta)**13 - 6.20264862173345e+30*cos(theta)**11 + 2.99250591399421e+30*cos(theta)**9 - 6.529103812351e+29*cos(theta)**7 + 6.46750849336656e+28*cos(theta)**5 - 2.53627784053591e+27*cos(theta)**3 + 2.58803861279174e+25*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl30_m_minus_16(theta, phi):
    return 1.24020738463486e-23*(1.0 - cos(theta)**2)**8*(3.3512478817058e+29*cos(theta)**14 - 5.16887385144454e+29*cos(theta)**12 + 2.99250591399421e+29*cos(theta)**10 - 8.16137976543875e+28*cos(theta)**8 + 1.07791808222776e+28*cos(theta)**6 - 6.34069460133976e+26*cos(theta)**4 + 1.29401930639587e+25*cos(theta)**2 - 3.93318938114246e+22)*sin(16*phi)

#@torch.jit.script
def Yl30_m_minus_15(theta, phi):
    return 3.25775828793813e-22*(1.0 - cos(theta)**2)**7.5*(2.23416525447054e+28*cos(theta)**15 - 3.9760568088035e+28*cos(theta)**13 + 2.72045992181292e+28*cos(theta)**11 - 9.06819973937639e+27*cos(theta)**9 + 1.53988297461109e+27*cos(theta)**7 - 1.26813892026795e+26*cos(theta)**5 + 4.31339768798623e+24*cos(theta)**3 - 3.93318938114246e+22*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl30_m_minus_14(theta, phi):
    return 8.74148278331158e-21*(1.0 - cos(theta)**2)**7*(1.39635328404408e+27*cos(theta)**16 - 2.84004057771678e+27*cos(theta)**14 + 2.2670499348441e+27*cos(theta)**12 - 9.06819973937639e+26*cos(theta)**10 + 1.92485371826386e+26*cos(theta)**8 - 2.11356486711326e+25*cos(theta)**6 + 1.07834942199656e+24*cos(theta)**4 - 1.96659469057123e+22*cos(theta)**2 + 5.46276302936453e+19)*sin(14*phi)

#@torch.jit.script
def Yl30_m_minus_13(theta, phi):
    return 2.39075958422627e-19*(1.0 - cos(theta)**2)**6.5*(8.21384284731815e+25*cos(theta)**17 - 1.89336038514452e+26*cos(theta)**15 + 1.74388456526469e+26*cos(theta)**13 - 8.24381794488763e+25*cos(theta)**11 + 2.13872635362651e+25*cos(theta)**9 - 3.01937838159036e+24*cos(theta)**7 + 2.15669884399312e+23*cos(theta)**5 - 6.55531563523744e+21*cos(theta)**3 + 5.46276302936453e+19*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl30_m_minus_12(theta, phi):
    return 6.65129768956931e-18*(1.0 - cos(theta)**2)**6*(4.56324602628786e+24*cos(theta)**18 - 1.18335024071533e+25*cos(theta)**16 + 1.24563183233192e+25*cos(theta)**14 - 6.86984828740636e+24*cos(theta)**12 + 2.13872635362651e+24*cos(theta)**10 - 3.77422297698795e+23*cos(theta)**8 + 3.59449807332186e+22*cos(theta)**6 - 1.63882890880936e+21*cos(theta)**4 + 2.73138151468227e+19*cos(theta)**2 - 7.05783337127201e+16)*sin(12*phi)

#@torch.jit.script
def Yl30_m_minus_11(theta, phi):
    return 1.87891801956087e-16*(1.0 - cos(theta)**2)**5.5*(2.40170843488835e+23*cos(theta)**19 - 6.96088376891368e+23*cos(theta)**17 + 8.30421221554615e+23*cos(theta)**15 - 5.28449868262028e+23*cos(theta)**13 + 1.94429668511501e+23*cos(theta)**11 - 4.19358108554217e+22*cos(theta)**9 + 5.13499724760266e+21*cos(theta)**7 - 3.27765781761872e+20*cos(theta)**5 + 9.10460504894089e+18*cos(theta)**3 - 7.05783337127201e+16*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl30_m_minus_10(theta, phi):
    return 5.38040239932763e-15*(1.0 - cos(theta)**2)**5*(1.20085421744417e+22*cos(theta)**20 - 3.86715764939649e+22*cos(theta)**18 + 5.19013263471634e+22*cos(theta)**16 - 3.77464191615734e+22*cos(theta)**14 + 1.62024723759584e+22*cos(theta)**12 - 4.19358108554217e+21*cos(theta)**10 + 6.41874655950332e+20*cos(theta)**8 - 5.46276302936453e+19*cos(theta)**6 + 2.27615126223522e+18*cos(theta)**4 - 3.528916685636e+16*cos(theta)**2 + 86071138674048.8)*sin(10*phi)

#@torch.jit.script
def Yl30_m_minus_9(theta, phi):
    return 1.55938876429517e-13*(1.0 - cos(theta)**2)**4.5*(5.71835341640083e+20*cos(theta)**21 - 2.03534613126131e+21*cos(theta)**19 + 3.05301919689197e+21*cos(theta)**17 - 2.51642794410489e+21*cos(theta)**15 + 1.24634402891988e+21*cos(theta)**13 - 3.81234644140197e+20*cos(theta)**11 + 7.13194062167036e+19*cos(theta)**9 - 7.80394718480647e+18*cos(theta)**7 + 4.55230252447044e+17*cos(theta)**5 - 1.17630556187867e+16*cos(theta)**3 + 86071138674048.8*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl30_m_minus_8(theta, phi):
    return 4.56770496751288e-12*(1.0 - cos(theta)**2)**4*(2.59925155290947e+19*cos(theta)**22 - 1.01767306563066e+20*cos(theta)**20 + 1.69612177605109e+20*cos(theta)**18 - 1.57276746506556e+20*cos(theta)**16 + 8.90245734942769e+19*cos(theta)**14 - 3.17695536783498e+19*cos(theta)**12 + 7.13194062167036e+18*cos(theta)**10 - 9.75493398100809e+17*cos(theta)**8 + 7.58717087411741e+16*cos(theta)**6 - 2.94076390469667e+15*cos(theta)**4 + 43035569337024.4*cos(theta)**2 - 100316012440.616)*sin(8*phi)

#@torch.jit.script
def Yl30_m_minus_7(theta, phi):
    return 1.3503730468945e-10*(1.0 - cos(theta)**2)**3.5*(1.1301093708302e+18*cos(theta)**23 - 4.84606221728884e+18*cos(theta)**21 + 8.92695671605838e+18*cos(theta)**19 - 9.25157332391505e+18*cos(theta)**17 + 5.93497156628513e+18*cos(theta)**15 - 2.44381182141152e+18*cos(theta)**13 + 6.48358238333669e+17*cos(theta)**11 - 1.08388155344534e+17*cos(theta)**9 + 1.08388155344534e+16*cos(theta)**7 - 588152780939334.0*cos(theta)**5 + 14345189779008.1*cos(theta)**3 - 100316012440.616*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl30_m_minus_6(theta, phi):
    return 4.02402104966148e-9*(1.0 - cos(theta)**2)**3*(4.70878904512584e+16*cos(theta)**24 - 2.20275555331311e+17*cos(theta)**22 + 4.46347835802919e+17*cos(theta)**20 - 5.13976295773058e+17*cos(theta)**18 + 3.7093572289282e+17*cos(theta)**16 - 1.7455798724368e+17*cos(theta)**14 + 5.40298531944724e+16*cos(theta)**12 - 1.08388155344534e+16*cos(theta)**10 + 1.35485194180668e+15*cos(theta)**8 - 98025463489889.0*cos(theta)**6 + 3586297444752.04*cos(theta)**4 - 50158006220.3082*cos(theta)**2 + 112968482.478172)*sin(6*phi)

#@torch.jit.script
def Yl30_m_minus_5(theta, phi):
    return 1.20720631489845e-7*(1.0 - cos(theta)**2)**2.5*(1.88351561805034e+15*cos(theta)**25 - 9.57719805788307e+15*cos(theta)**23 + 2.1254658847758e+16*cos(theta)**21 - 2.70513839880557e+16*cos(theta)**19 + 2.181974840546e+16*cos(theta)**17 - 1.16371991495787e+16*cos(theta)**15 + 4.15614255342096e+15*cos(theta)**13 - 985346866768494.0*cos(theta)**11 + 150539104645187.0*cos(theta)**9 - 14003637641412.7*cos(theta)**7 + 717259488950.407*cos(theta)**5 - 16719335406.7694*cos(theta)**3 + 112968482.478172*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl30_m_minus_4(theta, phi):
    return 3.64168346911826e-6*(1.0 - cos(theta)**2)**2*(72442908386551.5*cos(theta)**26 - 399049919078461.0*cos(theta)**24 + 966120856716275.0*cos(theta)**22 - 1.35256919940279e+15*cos(theta)**20 + 1.21220824474778e+15*cos(theta)**18 - 727324946848667.0*cos(theta)**16 + 296867325244354.0*cos(theta)**14 - 82112238897374.5*cos(theta)**12 + 15053910464518.7*cos(theta)**10 - 1750454705176.59*cos(theta)**8 + 119543248158.401*cos(theta)**6 - 4179833851.69235*cos(theta)**4 + 56484241.2390858*cos(theta)**2 - 124141.189536452)*sin(4*phi)

#@torch.jit.script
def Yl30_m_minus_3(theta, phi):
    return 0.000110337600540934*(1.0 - cos(theta)**2)**1.5*(2683070680983.39*cos(theta)**27 - 15961996763138.5*cos(theta)**25 + 42005254639838.0*cos(theta)**23 - 64408057114418.3*cos(theta)**21 + 63800433934093.6*cos(theta)**19 - 42783820402862.8*cos(theta)**17 + 19791155016290.3*cos(theta)**15 - 6316326069028.81*cos(theta)**13 + 1368537314956.24*cos(theta)**11 - 194494967241.843*cos(theta)**9 + 17077606879.7716*cos(theta)**7 - 835966770.33847*cos(theta)**5 + 18828080.4130286*cos(theta)**3 - 124141.189536452*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl30_m_minus_2(theta, phi):
    return 0.00335397268176902*(1.0 - cos(theta)**2)*(95823952892.2638*cos(theta)**28 - 613922952428.402*cos(theta)**26 + 1750218943326.59*cos(theta)**24 - 2927638959746.29*cos(theta)**22 + 3190021696704.68*cos(theta)**20 - 2376878911270.15*cos(theta)**18 + 1236947188518.14*cos(theta)**16 - 451166147787.772*cos(theta)**14 + 114044776246.354*cos(theta)**12 - 19449496724.1843*cos(theta)**10 + 2134700859.97145*cos(theta)**8 - 139327795.056412*cos(theta)**6 + 4707020.10325715*cos(theta)**4 - 62070.5947682261*cos(theta)**2 + 134.351936727762)*sin(2*phi)

#@torch.jit.script
def Yl30_m_minus_1(theta, phi):
    return 0.102172379790475*(1.0 - cos(theta)**2)**0.5*(3304274237.66427*cos(theta)**29 - 22737887126.9779*cos(theta)**27 + 70008757733.0634*cos(theta)**25 - 127288650423.752*cos(theta)**23 + 151905795081.175*cos(theta)**21 - 125098890066.85*cos(theta)**19 + 72761599324.5966*cos(theta)**17 - 30077743185.8515*cos(theta)**15 + 8772675095.87335*cos(theta)**13 - 1768136065.83494*cos(theta)**11 + 237188984.441272*cos(theta)**9 - 19903970.7223445*cos(theta)**7 + 941404.02065143*cos(theta)**5 - 20690.1982560754*cos(theta)**3 + 134.351936727762*cos(theta))*sin(phi)

#@torch.jit.script
def Yl30_m0(theta, phi):
    return 762368051.047141*cos(theta)**30 - 5620849189.92384*cos(theta)**28 + 18637552577.1159*cos(theta)**26 - 36710330833.7131*cos(theta)**24 + 47792694858.985*cos(theta)**22 - 43294558872.257*cos(theta)**20 + 27979476822.2069*cos(theta)**18 - 13011732382.3637*cos(theta)**16 + 4337244127.45456*cos(theta)**14 - 1019868774.15598*cos(theta)**12 + 164173997.790963*cos(theta)**10 - 17221048.7193318*cos(theta)**8 + 1086012.0813993*cos(theta)**6 - 35802.5960900869*cos(theta)**4 + 464.968780390739*cos(theta)**2 - 0.999932861055352

#@torch.jit.script
def Yl30_m1(theta, phi):
    return 0.102172379790475*(1.0 - cos(theta)**2)**0.5*(3304274237.66427*cos(theta)**29 - 22737887126.9779*cos(theta)**27 + 70008757733.0634*cos(theta)**25 - 127288650423.752*cos(theta)**23 + 151905795081.175*cos(theta)**21 - 125098890066.85*cos(theta)**19 + 72761599324.5966*cos(theta)**17 - 30077743185.8515*cos(theta)**15 + 8772675095.87335*cos(theta)**13 - 1768136065.83494*cos(theta)**11 + 237188984.441272*cos(theta)**9 - 19903970.7223445*cos(theta)**7 + 941404.02065143*cos(theta)**5 - 20690.1982560754*cos(theta)**3 + 134.351936727762*cos(theta))*cos(phi)

#@torch.jit.script
def Yl30_m2(theta, phi):
    return 0.00335397268176902*(1.0 - cos(theta)**2)*(95823952892.2638*cos(theta)**28 - 613922952428.402*cos(theta)**26 + 1750218943326.59*cos(theta)**24 - 2927638959746.29*cos(theta)**22 + 3190021696704.68*cos(theta)**20 - 2376878911270.15*cos(theta)**18 + 1236947188518.14*cos(theta)**16 - 451166147787.772*cos(theta)**14 + 114044776246.354*cos(theta)**12 - 19449496724.1843*cos(theta)**10 + 2134700859.97145*cos(theta)**8 - 139327795.056412*cos(theta)**6 + 4707020.10325715*cos(theta)**4 - 62070.5947682261*cos(theta)**2 + 134.351936727762)*cos(2*phi)

#@torch.jit.script
def Yl30_m3(theta, phi):
    return 0.000110337600540934*(1.0 - cos(theta)**2)**1.5*(2683070680983.39*cos(theta)**27 - 15961996763138.5*cos(theta)**25 + 42005254639838.0*cos(theta)**23 - 64408057114418.3*cos(theta)**21 + 63800433934093.6*cos(theta)**19 - 42783820402862.8*cos(theta)**17 + 19791155016290.3*cos(theta)**15 - 6316326069028.81*cos(theta)**13 + 1368537314956.24*cos(theta)**11 - 194494967241.843*cos(theta)**9 + 17077606879.7716*cos(theta)**7 - 835966770.33847*cos(theta)**5 + 18828080.4130286*cos(theta)**3 - 124141.189536452*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl30_m4(theta, phi):
    return 3.64168346911826e-6*(1.0 - cos(theta)**2)**2*(72442908386551.5*cos(theta)**26 - 399049919078461.0*cos(theta)**24 + 966120856716275.0*cos(theta)**22 - 1.35256919940279e+15*cos(theta)**20 + 1.21220824474778e+15*cos(theta)**18 - 727324946848667.0*cos(theta)**16 + 296867325244354.0*cos(theta)**14 - 82112238897374.5*cos(theta)**12 + 15053910464518.7*cos(theta)**10 - 1750454705176.59*cos(theta)**8 + 119543248158.401*cos(theta)**6 - 4179833851.69235*cos(theta)**4 + 56484241.2390858*cos(theta)**2 - 124141.189536452)*cos(4*phi)

#@torch.jit.script
def Yl30_m5(theta, phi):
    return 1.20720631489845e-7*(1.0 - cos(theta)**2)**2.5*(1.88351561805034e+15*cos(theta)**25 - 9.57719805788307e+15*cos(theta)**23 + 2.1254658847758e+16*cos(theta)**21 - 2.70513839880557e+16*cos(theta)**19 + 2.181974840546e+16*cos(theta)**17 - 1.16371991495787e+16*cos(theta)**15 + 4.15614255342096e+15*cos(theta)**13 - 985346866768494.0*cos(theta)**11 + 150539104645187.0*cos(theta)**9 - 14003637641412.7*cos(theta)**7 + 717259488950.407*cos(theta)**5 - 16719335406.7694*cos(theta)**3 + 112968482.478172*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl30_m6(theta, phi):
    return 4.02402104966148e-9*(1.0 - cos(theta)**2)**3*(4.70878904512584e+16*cos(theta)**24 - 2.20275555331311e+17*cos(theta)**22 + 4.46347835802919e+17*cos(theta)**20 - 5.13976295773058e+17*cos(theta)**18 + 3.7093572289282e+17*cos(theta)**16 - 1.7455798724368e+17*cos(theta)**14 + 5.40298531944724e+16*cos(theta)**12 - 1.08388155344534e+16*cos(theta)**10 + 1.35485194180668e+15*cos(theta)**8 - 98025463489889.0*cos(theta)**6 + 3586297444752.04*cos(theta)**4 - 50158006220.3082*cos(theta)**2 + 112968482.478172)*cos(6*phi)

#@torch.jit.script
def Yl30_m7(theta, phi):
    return 1.3503730468945e-10*(1.0 - cos(theta)**2)**3.5*(1.1301093708302e+18*cos(theta)**23 - 4.84606221728884e+18*cos(theta)**21 + 8.92695671605838e+18*cos(theta)**19 - 9.25157332391505e+18*cos(theta)**17 + 5.93497156628513e+18*cos(theta)**15 - 2.44381182141152e+18*cos(theta)**13 + 6.48358238333669e+17*cos(theta)**11 - 1.08388155344534e+17*cos(theta)**9 + 1.08388155344534e+16*cos(theta)**7 - 588152780939334.0*cos(theta)**5 + 14345189779008.1*cos(theta)**3 - 100316012440.616*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl30_m8(theta, phi):
    return 4.56770496751288e-12*(1.0 - cos(theta)**2)**4*(2.59925155290947e+19*cos(theta)**22 - 1.01767306563066e+20*cos(theta)**20 + 1.69612177605109e+20*cos(theta)**18 - 1.57276746506556e+20*cos(theta)**16 + 8.90245734942769e+19*cos(theta)**14 - 3.17695536783498e+19*cos(theta)**12 + 7.13194062167036e+18*cos(theta)**10 - 9.75493398100809e+17*cos(theta)**8 + 7.58717087411741e+16*cos(theta)**6 - 2.94076390469667e+15*cos(theta)**4 + 43035569337024.4*cos(theta)**2 - 100316012440.616)*cos(8*phi)

#@torch.jit.script
def Yl30_m9(theta, phi):
    return 1.55938876429517e-13*(1.0 - cos(theta)**2)**4.5*(5.71835341640083e+20*cos(theta)**21 - 2.03534613126131e+21*cos(theta)**19 + 3.05301919689197e+21*cos(theta)**17 - 2.51642794410489e+21*cos(theta)**15 + 1.24634402891988e+21*cos(theta)**13 - 3.81234644140197e+20*cos(theta)**11 + 7.13194062167036e+19*cos(theta)**9 - 7.80394718480647e+18*cos(theta)**7 + 4.55230252447044e+17*cos(theta)**5 - 1.17630556187867e+16*cos(theta)**3 + 86071138674048.8*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl30_m10(theta, phi):
    return 5.38040239932763e-15*(1.0 - cos(theta)**2)**5*(1.20085421744417e+22*cos(theta)**20 - 3.86715764939649e+22*cos(theta)**18 + 5.19013263471634e+22*cos(theta)**16 - 3.77464191615734e+22*cos(theta)**14 + 1.62024723759584e+22*cos(theta)**12 - 4.19358108554217e+21*cos(theta)**10 + 6.41874655950332e+20*cos(theta)**8 - 5.46276302936453e+19*cos(theta)**6 + 2.27615126223522e+18*cos(theta)**4 - 3.528916685636e+16*cos(theta)**2 + 86071138674048.8)*cos(10*phi)

#@torch.jit.script
def Yl30_m11(theta, phi):
    return 1.87891801956087e-16*(1.0 - cos(theta)**2)**5.5*(2.40170843488835e+23*cos(theta)**19 - 6.96088376891368e+23*cos(theta)**17 + 8.30421221554615e+23*cos(theta)**15 - 5.28449868262028e+23*cos(theta)**13 + 1.94429668511501e+23*cos(theta)**11 - 4.19358108554217e+22*cos(theta)**9 + 5.13499724760266e+21*cos(theta)**7 - 3.27765781761872e+20*cos(theta)**5 + 9.10460504894089e+18*cos(theta)**3 - 7.05783337127201e+16*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl30_m12(theta, phi):
    return 6.65129768956931e-18*(1.0 - cos(theta)**2)**6*(4.56324602628786e+24*cos(theta)**18 - 1.18335024071533e+25*cos(theta)**16 + 1.24563183233192e+25*cos(theta)**14 - 6.86984828740636e+24*cos(theta)**12 + 2.13872635362651e+24*cos(theta)**10 - 3.77422297698795e+23*cos(theta)**8 + 3.59449807332186e+22*cos(theta)**6 - 1.63882890880936e+21*cos(theta)**4 + 2.73138151468227e+19*cos(theta)**2 - 7.05783337127201e+16)*cos(12*phi)

#@torch.jit.script
def Yl30_m13(theta, phi):
    return 2.39075958422627e-19*(1.0 - cos(theta)**2)**6.5*(8.21384284731815e+25*cos(theta)**17 - 1.89336038514452e+26*cos(theta)**15 + 1.74388456526469e+26*cos(theta)**13 - 8.24381794488763e+25*cos(theta)**11 + 2.13872635362651e+25*cos(theta)**9 - 3.01937838159036e+24*cos(theta)**7 + 2.15669884399312e+23*cos(theta)**5 - 6.55531563523744e+21*cos(theta)**3 + 5.46276302936453e+19*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl30_m14(theta, phi):
    return 8.74148278331158e-21*(1.0 - cos(theta)**2)**7*(1.39635328404408e+27*cos(theta)**16 - 2.84004057771678e+27*cos(theta)**14 + 2.2670499348441e+27*cos(theta)**12 - 9.06819973937639e+26*cos(theta)**10 + 1.92485371826386e+26*cos(theta)**8 - 2.11356486711326e+25*cos(theta)**6 + 1.07834942199656e+24*cos(theta)**4 - 1.96659469057123e+22*cos(theta)**2 + 5.46276302936453e+19)*cos(14*phi)

#@torch.jit.script
def Yl30_m15(theta, phi):
    return 3.25775828793813e-22*(1.0 - cos(theta)**2)**7.5*(2.23416525447054e+28*cos(theta)**15 - 3.9760568088035e+28*cos(theta)**13 + 2.72045992181292e+28*cos(theta)**11 - 9.06819973937639e+27*cos(theta)**9 + 1.53988297461109e+27*cos(theta)**7 - 1.26813892026795e+26*cos(theta)**5 + 4.31339768798623e+24*cos(theta)**3 - 3.93318938114246e+22*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl30_m16(theta, phi):
    return 1.24020738463486e-23*(1.0 - cos(theta)**2)**8*(3.3512478817058e+29*cos(theta)**14 - 5.16887385144454e+29*cos(theta)**12 + 2.99250591399421e+29*cos(theta)**10 - 8.16137976543875e+28*cos(theta)**8 + 1.07791808222776e+28*cos(theta)**6 - 6.34069460133976e+26*cos(theta)**4 + 1.29401930639587e+25*cos(theta)**2 - 3.93318938114246e+22)*cos(16*phi)

#@torch.jit.script
def Yl30_m17(theta, phi):
    return 4.83483175810931e-25*(1.0 - cos(theta)**2)**8.5*(4.69174703438813e+30*cos(theta)**13 - 6.20264862173345e+30*cos(theta)**11 + 2.99250591399421e+30*cos(theta)**9 - 6.529103812351e+29*cos(theta)**7 + 6.46750849336656e+28*cos(theta)**5 - 2.53627784053591e+27*cos(theta)**3 + 2.58803861279174e+25*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl30_m18(theta, phi):
    return 1.93548170846062e-26*(1.0 - cos(theta)**2)**9*(6.09927114470456e+31*cos(theta)**12 - 6.8229134839068e+31*cos(theta)**10 + 2.69325532259479e+31*cos(theta)**8 - 4.5703726686457e+30*cos(theta)**6 + 3.23375424668328e+29*cos(theta)**4 - 7.60883352160772e+27*cos(theta)**2 + 2.58803861279174e+25)*cos(18*phi)

#@torch.jit.script
def Yl30_m19(theta, phi):
    return 7.98179203850954e-28*(1.0 - cos(theta)**2)**9.5*(7.31912537364547e+32*cos(theta)**11 - 6.8229134839068e+32*cos(theta)**9 + 2.15460425807583e+32*cos(theta)**7 - 2.74222360118742e+31*cos(theta)**5 + 1.29350169867331e+30*cos(theta)**3 - 1.52176670432154e+28*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl30_m20(theta, phi):
    return 3.40344756082348e-29*(1.0 - cos(theta)**2)**10*(8.05103791101002e+33*cos(theta)**10 - 6.14062213551612e+33*cos(theta)**8 + 1.50822298065308e+33*cos(theta)**6 - 1.37111180059371e+32*cos(theta)**4 + 3.88050509601994e+30*cos(theta)**2 - 1.52176670432154e+28)*cos(20*phi)

#@torch.jit.script
def Yl30_m21(theta, phi):
    return 1.5070719110102e-30*(1.0 - cos(theta)**2)**10.5*(8.05103791101002e+34*cos(theta)**9 - 4.9124977084129e+34*cos(theta)**7 + 9.04933788391849e+33*cos(theta)**5 - 5.48444720237484e+32*cos(theta)**3 + 7.76101019203987e+30*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl30_m22(theta, phi):
    return 6.96644237302409e-32*(1.0 - cos(theta)**2)**11*(7.24593411990902e+35*cos(theta)**8 - 3.43874839588903e+35*cos(theta)**6 + 4.52466894195925e+34*cos(theta)**4 - 1.64533416071245e+33*cos(theta)**2 + 7.76101019203987e+30)*cos(22*phi)

#@torch.jit.script
def Yl30_m23(theta, phi):
    return 3.38320349392245e-33*(1.0 - cos(theta)**2)**11.5*(5.79674729592722e+36*cos(theta)**7 - 2.06324903753342e+36*cos(theta)**5 + 1.8098675767837e+35*cos(theta)**3 - 3.29066832142491e+33*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl30_m24(theta, phi):
    return 1.74013210905229e-34*(1.0 - cos(theta)**2)**12*(4.05772310714905e+37*cos(theta)**6 - 1.03162451876671e+37*cos(theta)**4 + 5.42960273035109e+35*cos(theta)**2 - 3.29066832142491e+33)*cos(24*phi)

#@torch.jit.script
def Yl30_m25(theta, phi):
    return 9.57911199299742e-36*(1.0 - cos(theta)**2)**12.5*(2.43463386428943e+38*cos(theta)**5 - 4.12649807506683e+37*cos(theta)**3 + 1.08592054607022e+36*cos(theta))*cos(25*phi)

#@torch.jit.script
def Yl30_m26(theta, phi):
    return 5.72461435302436e-37*(1.0 - cos(theta)**2)**13*(1.21731693214472e+39*cos(theta)**4 - 1.23794942252005e+38*cos(theta)**2 + 1.08592054607022e+36)*cos(26*phi)

#@torch.jit.script
def Yl30_m27(theta, phi):
    return 3.79121847114987e-38*(1.0 - cos(theta)**2)**13.5*(4.86926772857886e+39*cos(theta)**3 - 2.4758988450401e+38*cos(theta))*cos(27*phi)

#@torch.jit.script
def Yl30_m28(theta, phi):
    return 2.87411530575892e-39*(1.0 - cos(theta)**2)**14*(1.46078031857366e+40*cos(theta)**2 - 2.4758988450401e+38)*cos(28*phi)

#@torch.jit.script
def Yl30_m29(theta, phi):
    return 7.72997498267602*(1.0 - cos(theta)**2)**14.5*cos(29*phi)*cos(theta)

#@torch.jit.script
def Yl30_m30(theta, phi):
    return 0.997935479150139*(1.0 - cos(theta)**2)**15*cos(30*phi)

#@torch.jit.script
def Yl31_m_minus_31(theta, phi):
    return 1.00595115393533*(1.0 - cos(theta)**2)**15.5*sin(31*phi)

#@torch.jit.script
def Yl31_m_minus_30(theta, phi):
    return 7.92086730695805*(1.0 - cos(theta)**2)**15*sin(30*phi)*cos(theta)

#@torch.jit.script
def Yl31_m_minus_29(theta, phi):
    return 4.90916821524168e-41*(1.0 - cos(theta)**2)**14.5*(8.91075994329932e+41*cos(theta)**2 - 1.46078031857366e+40)*sin(29*phi)

#@torch.jit.script
def Yl31_m_minus_28(theta, phi):
    return 6.58634030535703e-40*(1.0 - cos(theta)**2)**14*(2.97025331443311e+41*cos(theta)**3 - 1.46078031857366e+40*cos(theta))*sin(28*phi)

#@torch.jit.script
def Yl31_m_minus_27(theta, phi):
    return 1.01181279661018e-38*(1.0 - cos(theta)**2)**13.5*(7.42563328608276e+40*cos(theta)**4 - 7.30390159286829e+39*cos(theta)**2 + 6.18974711260025e+37)*sin(27*phi)

#@torch.jit.script
def Yl31_m_minus_26(theta, phi):
    return 1.72305510434632e-37*(1.0 - cos(theta)**2)**13*(1.48512665721655e+40*cos(theta)**5 - 2.43463386428943e+39*cos(theta)**3 + 6.18974711260025e+37*cos(theta))*sin(26*phi)

#@torch.jit.script
def Yl31_m_minus_25(theta, phi):
    return 3.18648750393588e-36*(1.0 - cos(theta)**2)**12.5*(2.47521109536092e+39*cos(theta)**6 - 6.08658466072358e+38*cos(theta)**4 + 3.09487355630012e+37*cos(theta)**2 - 1.8098675767837e+35)*sin(25*phi)

#@torch.jit.script
def Yl31_m_minus_24(theta, phi):
    return 6.30892338215793e-35*(1.0 - cos(theta)**2)**12*(3.5360158505156e+38*cos(theta)**7 - 1.21731693214472e+38*cos(theta)**5 + 1.03162451876671e+37*cos(theta)**3 - 1.8098675767837e+35*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl31_m_minus_23(theta, phi):
    return 1.32337093312696e-33*(1.0 - cos(theta)**2)**11.5*(4.4200198131445e+37*cos(theta)**8 - 2.02886155357453e+37*cos(theta)**6 + 2.57906129691677e+36*cos(theta)**4 - 9.04933788391849e+34*cos(theta)**2 + 4.11333540178113e+32)*sin(23*phi)

#@torch.jit.script
def Yl31_m_minus_22(theta, phi):
    return 2.9174251739327e-32*(1.0 - cos(theta)**2)**11*(4.91113312571611e+36*cos(theta)**9 - 2.89837364796361e+36*cos(theta)**7 + 5.15812259383354e+35*cos(theta)**5 - 3.01644596130616e+34*cos(theta)**3 + 4.11333540178113e+32*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl31_m_minus_21(theta, phi):
    return 6.7164171342413e-31*(1.0 - cos(theta)**2)**10.5*(4.91113312571611e+35*cos(theta)**10 - 3.62296705995451e+35*cos(theta)**8 + 8.59687098972257e+34*cos(theta)**6 - 7.54111490326541e+33*cos(theta)**4 + 2.05666770089057e+32*cos(theta)**2 - 7.76101019203987e+29)*sin(21*phi)

#@torch.jit.script
def Yl31_m_minus_20(theta, phi):
    return 1.60633334701383e-29*(1.0 - cos(theta)**2)**10*(4.46466647792374e+34*cos(theta)**11 - 4.02551895550501e+34*cos(theta)**9 + 1.22812442710322e+34*cos(theta)**7 - 1.50822298065308e+33*cos(theta)**5 + 6.85555900296855e+31*cos(theta)**3 - 7.76101019203987e+29*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl31_m_minus_19(theta, phi):
    return 3.97384923581397e-28*(1.0 - cos(theta)**2)**9.5*(3.72055539826978e+33*cos(theta)**12 - 4.02551895550501e+33*cos(theta)**10 + 1.53515553387903e+33*cos(theta)**8 - 2.51370496775514e+32*cos(theta)**6 + 1.71388975074214e+31*cos(theta)**4 - 3.88050509601994e+29*cos(theta)**2 + 1.26813892026795e+27)*sin(19*phi)

#@torch.jit.script
def Yl31_m_minus_18(theta, phi):
    return 1.01313673987456e-26*(1.0 - cos(theta)**2)**9*(2.86196569097676e+32*cos(theta)**13 - 3.65956268682274e+32*cos(theta)**11 + 1.7057283709767e+32*cos(theta)**9 - 3.59100709679305e+31*cos(theta)**7 + 3.42777950148428e+30*cos(theta)**5 - 1.29350169867331e+29*cos(theta)**3 + 1.26813892026795e+27*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl31_m_minus_17(theta, phi):
    return 2.6535673965946e-25*(1.0 - cos(theta)**2)**8.5*(2.04426120784054e+31*cos(theta)**14 - 3.04963557235228e+31*cos(theta)**12 + 1.7057283709767e+31*cos(theta)**10 - 4.48875887099132e+30*cos(theta)**8 + 5.71296583580713e+29*cos(theta)**6 - 3.23375424668328e+28*cos(theta)**4 + 6.34069460133976e+26*cos(theta)**2 - 1.84859900913696e+24)*sin(17*phi)

#@torch.jit.script
def Yl31_m_minus_16(theta, phi):
    return 7.12026849799521e-24*(1.0 - cos(theta)**2)**8*(1.36284080522703e+30*cos(theta)**15 - 2.34587351719406e+30*cos(theta)**13 + 1.55066215543336e+30*cos(theta)**11 - 4.98750985665702e+29*cos(theta)**9 + 8.16137976543875e+28*cos(theta)**7 - 6.46750849336656e+27*cos(theta)**5 + 2.11356486711325e+26*cos(theta)**3 - 1.84859900913696e+24*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl31_m_minus_15(theta, phi):
    return 1.95256405937486e-22*(1.0 - cos(theta)**2)**7.5*(8.51775503266892e+28*cos(theta)**16 - 1.6756239408529e+29*cos(theta)**14 + 1.29221846286114e+29*cos(theta)**12 - 4.98750985665702e+28*cos(theta)**10 + 1.02017247067984e+28*cos(theta)**8 - 1.07791808222776e+27*cos(theta)**6 + 5.28391216778314e+25*cos(theta)**4 - 9.24299504568479e+23*cos(theta)**2 + 2.45824336321404e+21)*sin(15*phi)

#@torch.jit.script
def Yl31_m_minus_14(theta, phi):
    return 5.46020147014982e-21*(1.0 - cos(theta)**2)**7*(5.01044413686407e+27*cos(theta)**17 - 1.11708262723527e+28*cos(theta)**15 + 9.94014202200874e+27*cos(theta)**13 - 4.5340998696882e+27*cos(theta)**11 + 1.13352496742205e+27*cos(theta)**9 - 1.53988297461109e+26*cos(theta)**7 + 1.05678243355663e+25*cos(theta)**5 - 3.0809983485616e+23*cos(theta)**3 + 2.45824336321404e+21*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl31_m_minus_13(theta, phi):
    return 1.5540005816166e-19*(1.0 - cos(theta)**2)**6.5*(2.78358007603559e+26*cos(theta)**18 - 6.98176642022042e+26*cos(theta)**16 + 7.10010144429196e+26*cos(theta)**14 - 3.7784165580735e+26*cos(theta)**12 + 1.13352496742205e+26*cos(theta)**10 - 1.92485371826386e+25*cos(theta)**8 + 1.76130405592771e+24*cos(theta)**6 - 7.70249587140399e+22*cos(theta)**4 + 1.22912168160702e+21*cos(theta)**2 - 3.03486834964696e+18)*sin(13*phi)

#@torch.jit.script
def Yl31_m_minus_12(theta, phi):
    return 4.49318515889086e-18*(1.0 - cos(theta)**2)**6*(1.46504214528189e+25*cos(theta)**19 - 4.10692142365907e+25*cos(theta)**17 + 4.7334009628613e+25*cos(theta)**15 - 2.90647427544115e+25*cos(theta)**13 + 1.03047724311095e+25*cos(theta)**11 - 2.13872635362651e+24*cos(theta)**9 + 2.5161486513253e+23*cos(theta)**7 - 1.5404991742808e+22*cos(theta)**5 + 4.0970722720234e+20*cos(theta)**3 - 3.03486834964696e+18*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl31_m_minus_11(theta, phi):
    return 1.31766054315921e-16*(1.0 - cos(theta)**2)**5.5*(7.32521072640946e+23*cos(theta)**20 - 2.28162301314393e+24*cos(theta)**18 + 2.95837560178832e+24*cos(theta)**16 - 2.07605305388654e+24*cos(theta)**14 + 8.58731035925795e+23*cos(theta)**12 - 2.13872635362651e+23*cos(theta)**10 + 3.14518581415663e+22*cos(theta)**8 - 2.56749862380133e+21*cos(theta)**6 + 1.02426806800585e+20*cos(theta)**4 - 1.51743417482348e+18*cos(theta)**2 + 3.528916685636e+15)*sin(11*phi)

#@torch.jit.script
def Yl31_m_minus_10(theta, phi):
    return 3.91325216255328e-15*(1.0 - cos(theta)**2)**5*(3.4881955840045e+22*cos(theta)**21 - 1.20085421744417e+23*cos(theta)**19 + 1.74022094222842e+23*cos(theta)**17 - 1.38403536925769e+23*cos(theta)**15 + 6.60562335327535e+22*cos(theta)**13 - 1.94429668511501e+22*cos(theta)**11 + 3.49465090461848e+21*cos(theta)**9 - 3.66785517685904e+20*cos(theta)**7 + 2.0485361360117e+19*cos(theta)**5 - 5.05811391607827e+17*cos(theta)**3 + 3.528916685636e+15*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl31_m_minus_9(theta, phi):
    return 1.17527934228125e-13*(1.0 - cos(theta)**2)**4.5*(1.58554344727477e+21*cos(theta)**22 - 6.00427108722087e+21*cos(theta)**20 + 9.66789412349123e+21*cos(theta)**18 - 8.65022105786057e+21*cos(theta)**16 + 4.71830239519667e+21*cos(theta)**14 - 1.62024723759584e+21*cos(theta)**12 + 3.49465090461848e+20*cos(theta)**10 - 4.5848189710738e+19*cos(theta)**8 + 3.41422689335283e+18*cos(theta)**6 - 1.26452847901957e+17*cos(theta)**4 + 1.764458342818e+15*cos(theta)**2 - 3912324485184.04)*sin(9*phi)

#@torch.jit.script
def Yl31_m_minus_8(theta, phi):
    return 3.56479874579423e-12*(1.0 - cos(theta)**2)**4*(6.89366716206424e+19*cos(theta)**23 - 2.85917670820041e+20*cos(theta)**21 + 5.08836532815328e+20*cos(theta)**19 - 5.08836532815328e+20*cos(theta)**17 + 3.14553493013112e+20*cos(theta)**15 - 1.24634402891988e+20*cos(theta)**13 + 3.17695536783498e+19*cos(theta)**11 - 5.09424330119312e+18*cos(theta)**9 + 4.87746699050405e+17*cos(theta)**7 - 2.52905695803914e+16*cos(theta)**5 + 588152780939334.0*cos(theta)**3 - 3912324485184.04*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl31_m_minus_7(theta, phi):
    return 1.09061870201015e-10*(1.0 - cos(theta)**2)**3.5*(2.87236131752677e+18*cos(theta)**24 - 1.29962577645473e+19*cos(theta)**22 + 2.54418266407664e+19*cos(theta)**20 - 2.82686962675182e+19*cos(theta)**18 + 1.96595933133195e+19*cos(theta)**16 - 8.90245734942769e+18*cos(theta)**14 + 2.64746280652915e+18*cos(theta)**12 - 5.09424330119312e+17*cos(theta)**10 + 6.09683373813006e+16*cos(theta)**8 - 4.21509493006523e+15*cos(theta)**6 + 147038195234833.0*cos(theta)**4 - 1956162242592.02*cos(theta)**2 + 4179833851.69235)*sin(7*phi)

#@torch.jit.script
def Yl31_m_minus_6(theta, phi):
    return 3.36151259928562e-9*(1.0 - cos(theta)**2)**3*(1.14894452701071e+17*cos(theta)**25 - 5.65054685415101e+17*cos(theta)**23 + 1.21151555432221e+18*cos(theta)**21 - 1.48782611934306e+18*cos(theta)**19 + 1.15644666548938e+18*cos(theta)**17 - 5.93497156628513e+17*cos(theta)**15 + 2.03650985117627e+17*cos(theta)**13 - 4.63113027381192e+16*cos(theta)**11 + 6.7742597090334e+15*cos(theta)**9 - 602156418580747.0*cos(theta)**7 + 29407639046966.7*cos(theta)**5 - 652054080864.006*cos(theta)**3 + 4179833851.69235*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl31_m_minus_5(theta, phi):
    return 1.04261094425773e-7*(1.0 - cos(theta)**2)**2.5*(4.41901741157964e+15*cos(theta)**26 - 2.35439452256292e+16*cos(theta)**24 + 5.50688888328277e+16*cos(theta)**22 - 7.43913059671532e+16*cos(theta)**20 + 6.42470369716323e+16*cos(theta)**18 - 3.7093572289282e+16*cos(theta)**16 + 1.45464989369733e+16*cos(theta)**14 - 3.8592752281766e+15*cos(theta)**12 + 677425970903340.0*cos(theta)**10 - 75269552322593.3*cos(theta)**8 + 4901273174494.45*cos(theta)**6 - 163013520216.002*cos(theta)**4 + 2089916925.84617*cos(theta)**2 - 4344941.63377583)*sin(5*phi)

#@torch.jit.script
def Yl31_m_minus_4(theta, phi):
    return 3.25053923036716e-6*(1.0 - cos(theta)**2)**2*(163667311539987.0*cos(theta)**27 - 941757809025169.0*cos(theta)**25 + 2.39429951447077e+15*cos(theta)**23 - 3.54244314129301e+15*cos(theta)**21 + 3.38142299850696e+15*cos(theta)**19 - 2.181974840546e+15*cos(theta)**17 + 969766595798223.0*cos(theta)**15 - 296867325244354.0*cos(theta)**13 + 61584179173030.9*cos(theta)**11 - 8363283591399.26*cos(theta)**9 + 700181882070.635*cos(theta)**7 - 32602704043.2003*cos(theta)**5 + 696638975.282058*cos(theta)**3 - 4344941.63377583*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl31_m_minus_3(theta, phi):
    return 0.000101757973556832*(1.0 - cos(theta)**2)**1.5*(5845261126428.09*cos(theta)**28 - 36221454193275.7*cos(theta)**26 + 99762479769615.3*cos(theta)**24 - 161020142786046.0*cos(theta)**22 + 169071149925348.0*cos(theta)**20 - 121220824474778.0*cos(theta)**18 + 60610412237388.9*cos(theta)**16 - 21204808946025.3*cos(theta)**14 + 5132014931085.91*cos(theta)**12 - 836328359139.926*cos(theta)**10 + 87522735258.8294*cos(theta)**8 - 5433784007.20005*cos(theta)**6 + 174159743.820515*cos(theta)**4 - 2172470.81688792*cos(theta)**2 + 4433.61391201615)*sin(3*phi)

#@torch.jit.script
def Yl31_m_minus_2(theta, phi):
    return 0.00319526518302305*(1.0 - cos(theta)**2)*(201560728497.52*cos(theta)**29 - 1341535340491.69*cos(theta)**27 + 3990499190784.61*cos(theta)**25 - 7000875773306.34*cos(theta)**23 + 8051007139302.29*cos(theta)**21 - 6380043393409.36*cos(theta)**19 + 3565318366905.23*cos(theta)**17 - 1413653929735.02*cos(theta)**15 + 394770379314.301*cos(theta)**13 - 76029850830.9023*cos(theta)**11 + 9724748362.09216*cos(theta)**9 - 776254858.171436*cos(theta)**7 + 34831948.7641029*cos(theta)**5 - 724156.938962638*cos(theta)**3 + 4433.61391201615*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl31_m_minus_1(theta, phi):
    return 0.100536671886138*(1.0 - cos(theta)**2)**0.5*(6718690949.91735*cos(theta)**30 - 47911976446.1319*cos(theta)**28 + 153480738107.101*cos(theta)**26 - 291703157221.098*cos(theta)**24 + 365954869968.286*cos(theta)**22 - 319002169670.468*cos(theta)**20 + 198073242605.846*cos(theta)**18 - 88353370608.4387*cos(theta)**16 + 28197884236.7358*cos(theta)**14 - 6335820902.57519*cos(theta)**12 + 972474836.209216*cos(theta)**10 - 97031857.2714295*cos(theta)**8 + 5805324.79401715*cos(theta)**6 - 181039.23474066*cos(theta)**4 + 2216.80695600808*cos(theta)**2 - 4.47839789092541)*sin(phi)

#@torch.jit.script
def Yl31_m0(theta, phi):
    return 1524537762.43789*cos(theta)**31 - 11621476385.797*cos(theta)**29 + 39985757734.1829*cos(theta)**27 - 82076029033.3228*cos(theta)**25 + 111921857772.713*cos(theta)**23 - 106853698175.458*cos(theta)**21 + 73330969336.0986*cos(theta)**19 - 36558588211.2912*cos(theta)**17 + 13223319140.2542*cos(theta)**15 - 3428267925.2511*cos(theta)**13 + 621871856.208339*cos(theta)**11 - 75838031.2449194*cos(theta)**9 + 5833694.71114765*cos(theta)**7 - 254693.532087527*cos(theta)**5 + 5197.82718545974*cos(theta)**3 - 31.5019829421802*cos(theta)

#@torch.jit.script
def Yl31_m1(theta, phi):
    return 0.100536671886138*(1.0 - cos(theta)**2)**0.5*(6718690949.91735*cos(theta)**30 - 47911976446.1319*cos(theta)**28 + 153480738107.101*cos(theta)**26 - 291703157221.098*cos(theta)**24 + 365954869968.286*cos(theta)**22 - 319002169670.468*cos(theta)**20 + 198073242605.846*cos(theta)**18 - 88353370608.4387*cos(theta)**16 + 28197884236.7358*cos(theta)**14 - 6335820902.57519*cos(theta)**12 + 972474836.209216*cos(theta)**10 - 97031857.2714295*cos(theta)**8 + 5805324.79401715*cos(theta)**6 - 181039.23474066*cos(theta)**4 + 2216.80695600808*cos(theta)**2 - 4.47839789092541)*cos(phi)

#@torch.jit.script
def Yl31_m2(theta, phi):
    return 0.00319526518302305*(1.0 - cos(theta)**2)*(201560728497.52*cos(theta)**29 - 1341535340491.69*cos(theta)**27 + 3990499190784.61*cos(theta)**25 - 7000875773306.34*cos(theta)**23 + 8051007139302.29*cos(theta)**21 - 6380043393409.36*cos(theta)**19 + 3565318366905.23*cos(theta)**17 - 1413653929735.02*cos(theta)**15 + 394770379314.301*cos(theta)**13 - 76029850830.9023*cos(theta)**11 + 9724748362.09216*cos(theta)**9 - 776254858.171436*cos(theta)**7 + 34831948.7641029*cos(theta)**5 - 724156.938962638*cos(theta)**3 + 4433.61391201615*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl31_m3(theta, phi):
    return 0.000101757973556832*(1.0 - cos(theta)**2)**1.5*(5845261126428.09*cos(theta)**28 - 36221454193275.7*cos(theta)**26 + 99762479769615.3*cos(theta)**24 - 161020142786046.0*cos(theta)**22 + 169071149925348.0*cos(theta)**20 - 121220824474778.0*cos(theta)**18 + 60610412237388.9*cos(theta)**16 - 21204808946025.3*cos(theta)**14 + 5132014931085.91*cos(theta)**12 - 836328359139.926*cos(theta)**10 + 87522735258.8294*cos(theta)**8 - 5433784007.20005*cos(theta)**6 + 174159743.820515*cos(theta)**4 - 2172470.81688792*cos(theta)**2 + 4433.61391201615)*cos(3*phi)

#@torch.jit.script
def Yl31_m4(theta, phi):
    return 3.25053923036716e-6*(1.0 - cos(theta)**2)**2*(163667311539987.0*cos(theta)**27 - 941757809025169.0*cos(theta)**25 + 2.39429951447077e+15*cos(theta)**23 - 3.54244314129301e+15*cos(theta)**21 + 3.38142299850696e+15*cos(theta)**19 - 2.181974840546e+15*cos(theta)**17 + 969766595798223.0*cos(theta)**15 - 296867325244354.0*cos(theta)**13 + 61584179173030.9*cos(theta)**11 - 8363283591399.26*cos(theta)**9 + 700181882070.635*cos(theta)**7 - 32602704043.2003*cos(theta)**5 + 696638975.282058*cos(theta)**3 - 4344941.63377583*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl31_m5(theta, phi):
    return 1.04261094425773e-7*(1.0 - cos(theta)**2)**2.5*(4.41901741157964e+15*cos(theta)**26 - 2.35439452256292e+16*cos(theta)**24 + 5.50688888328277e+16*cos(theta)**22 - 7.43913059671532e+16*cos(theta)**20 + 6.42470369716323e+16*cos(theta)**18 - 3.7093572289282e+16*cos(theta)**16 + 1.45464989369733e+16*cos(theta)**14 - 3.8592752281766e+15*cos(theta)**12 + 677425970903340.0*cos(theta)**10 - 75269552322593.3*cos(theta)**8 + 4901273174494.45*cos(theta)**6 - 163013520216.002*cos(theta)**4 + 2089916925.84617*cos(theta)**2 - 4344941.63377583)*cos(5*phi)

#@torch.jit.script
def Yl31_m6(theta, phi):
    return 3.36151259928562e-9*(1.0 - cos(theta)**2)**3*(1.14894452701071e+17*cos(theta)**25 - 5.65054685415101e+17*cos(theta)**23 + 1.21151555432221e+18*cos(theta)**21 - 1.48782611934306e+18*cos(theta)**19 + 1.15644666548938e+18*cos(theta)**17 - 5.93497156628513e+17*cos(theta)**15 + 2.03650985117627e+17*cos(theta)**13 - 4.63113027381192e+16*cos(theta)**11 + 6.7742597090334e+15*cos(theta)**9 - 602156418580747.0*cos(theta)**7 + 29407639046966.7*cos(theta)**5 - 652054080864.006*cos(theta)**3 + 4179833851.69235*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl31_m7(theta, phi):
    return 1.09061870201015e-10*(1.0 - cos(theta)**2)**3.5*(2.87236131752677e+18*cos(theta)**24 - 1.29962577645473e+19*cos(theta)**22 + 2.54418266407664e+19*cos(theta)**20 - 2.82686962675182e+19*cos(theta)**18 + 1.96595933133195e+19*cos(theta)**16 - 8.90245734942769e+18*cos(theta)**14 + 2.64746280652915e+18*cos(theta)**12 - 5.09424330119312e+17*cos(theta)**10 + 6.09683373813006e+16*cos(theta)**8 - 4.21509493006523e+15*cos(theta)**6 + 147038195234833.0*cos(theta)**4 - 1956162242592.02*cos(theta)**2 + 4179833851.69235)*cos(7*phi)

#@torch.jit.script
def Yl31_m8(theta, phi):
    return 3.56479874579423e-12*(1.0 - cos(theta)**2)**4*(6.89366716206424e+19*cos(theta)**23 - 2.85917670820041e+20*cos(theta)**21 + 5.08836532815328e+20*cos(theta)**19 - 5.08836532815328e+20*cos(theta)**17 + 3.14553493013112e+20*cos(theta)**15 - 1.24634402891988e+20*cos(theta)**13 + 3.17695536783498e+19*cos(theta)**11 - 5.09424330119312e+18*cos(theta)**9 + 4.87746699050405e+17*cos(theta)**7 - 2.52905695803914e+16*cos(theta)**5 + 588152780939334.0*cos(theta)**3 - 3912324485184.04*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl31_m9(theta, phi):
    return 1.17527934228125e-13*(1.0 - cos(theta)**2)**4.5*(1.58554344727477e+21*cos(theta)**22 - 6.00427108722087e+21*cos(theta)**20 + 9.66789412349123e+21*cos(theta)**18 - 8.65022105786057e+21*cos(theta)**16 + 4.71830239519667e+21*cos(theta)**14 - 1.62024723759584e+21*cos(theta)**12 + 3.49465090461848e+20*cos(theta)**10 - 4.5848189710738e+19*cos(theta)**8 + 3.41422689335283e+18*cos(theta)**6 - 1.26452847901957e+17*cos(theta)**4 + 1.764458342818e+15*cos(theta)**2 - 3912324485184.04)*cos(9*phi)

#@torch.jit.script
def Yl31_m10(theta, phi):
    return 3.91325216255328e-15*(1.0 - cos(theta)**2)**5*(3.4881955840045e+22*cos(theta)**21 - 1.20085421744417e+23*cos(theta)**19 + 1.74022094222842e+23*cos(theta)**17 - 1.38403536925769e+23*cos(theta)**15 + 6.60562335327535e+22*cos(theta)**13 - 1.94429668511501e+22*cos(theta)**11 + 3.49465090461848e+21*cos(theta)**9 - 3.66785517685904e+20*cos(theta)**7 + 2.0485361360117e+19*cos(theta)**5 - 5.05811391607827e+17*cos(theta)**3 + 3.528916685636e+15*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl31_m11(theta, phi):
    return 1.31766054315921e-16*(1.0 - cos(theta)**2)**5.5*(7.32521072640946e+23*cos(theta)**20 - 2.28162301314393e+24*cos(theta)**18 + 2.95837560178832e+24*cos(theta)**16 - 2.07605305388654e+24*cos(theta)**14 + 8.58731035925795e+23*cos(theta)**12 - 2.13872635362651e+23*cos(theta)**10 + 3.14518581415663e+22*cos(theta)**8 - 2.56749862380133e+21*cos(theta)**6 + 1.02426806800585e+20*cos(theta)**4 - 1.51743417482348e+18*cos(theta)**2 + 3.528916685636e+15)*cos(11*phi)

#@torch.jit.script
def Yl31_m12(theta, phi):
    return 4.49318515889086e-18*(1.0 - cos(theta)**2)**6*(1.46504214528189e+25*cos(theta)**19 - 4.10692142365907e+25*cos(theta)**17 + 4.7334009628613e+25*cos(theta)**15 - 2.90647427544115e+25*cos(theta)**13 + 1.03047724311095e+25*cos(theta)**11 - 2.13872635362651e+24*cos(theta)**9 + 2.5161486513253e+23*cos(theta)**7 - 1.5404991742808e+22*cos(theta)**5 + 4.0970722720234e+20*cos(theta)**3 - 3.03486834964696e+18*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl31_m13(theta, phi):
    return 1.5540005816166e-19*(1.0 - cos(theta)**2)**6.5*(2.78358007603559e+26*cos(theta)**18 - 6.98176642022042e+26*cos(theta)**16 + 7.10010144429196e+26*cos(theta)**14 - 3.7784165580735e+26*cos(theta)**12 + 1.13352496742205e+26*cos(theta)**10 - 1.92485371826386e+25*cos(theta)**8 + 1.76130405592771e+24*cos(theta)**6 - 7.70249587140399e+22*cos(theta)**4 + 1.22912168160702e+21*cos(theta)**2 - 3.03486834964696e+18)*cos(13*phi)

#@torch.jit.script
def Yl31_m14(theta, phi):
    return 5.46020147014982e-21*(1.0 - cos(theta)**2)**7*(5.01044413686407e+27*cos(theta)**17 - 1.11708262723527e+28*cos(theta)**15 + 9.94014202200874e+27*cos(theta)**13 - 4.5340998696882e+27*cos(theta)**11 + 1.13352496742205e+27*cos(theta)**9 - 1.53988297461109e+26*cos(theta)**7 + 1.05678243355663e+25*cos(theta)**5 - 3.0809983485616e+23*cos(theta)**3 + 2.45824336321404e+21*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl31_m15(theta, phi):
    return 1.95256405937486e-22*(1.0 - cos(theta)**2)**7.5*(8.51775503266892e+28*cos(theta)**16 - 1.6756239408529e+29*cos(theta)**14 + 1.29221846286114e+29*cos(theta)**12 - 4.98750985665702e+28*cos(theta)**10 + 1.02017247067984e+28*cos(theta)**8 - 1.07791808222776e+27*cos(theta)**6 + 5.28391216778314e+25*cos(theta)**4 - 9.24299504568479e+23*cos(theta)**2 + 2.45824336321404e+21)*cos(15*phi)

#@torch.jit.script
def Yl31_m16(theta, phi):
    return 7.12026849799521e-24*(1.0 - cos(theta)**2)**8*(1.36284080522703e+30*cos(theta)**15 - 2.34587351719406e+30*cos(theta)**13 + 1.55066215543336e+30*cos(theta)**11 - 4.98750985665702e+29*cos(theta)**9 + 8.16137976543875e+28*cos(theta)**7 - 6.46750849336656e+27*cos(theta)**5 + 2.11356486711325e+26*cos(theta)**3 - 1.84859900913696e+24*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl31_m17(theta, phi):
    return 2.6535673965946e-25*(1.0 - cos(theta)**2)**8.5*(2.04426120784054e+31*cos(theta)**14 - 3.04963557235228e+31*cos(theta)**12 + 1.7057283709767e+31*cos(theta)**10 - 4.48875887099132e+30*cos(theta)**8 + 5.71296583580713e+29*cos(theta)**6 - 3.23375424668328e+28*cos(theta)**4 + 6.34069460133976e+26*cos(theta)**2 - 1.84859900913696e+24)*cos(17*phi)

#@torch.jit.script
def Yl31_m18(theta, phi):
    return 1.01313673987456e-26*(1.0 - cos(theta)**2)**9*(2.86196569097676e+32*cos(theta)**13 - 3.65956268682274e+32*cos(theta)**11 + 1.7057283709767e+32*cos(theta)**9 - 3.59100709679305e+31*cos(theta)**7 + 3.42777950148428e+30*cos(theta)**5 - 1.29350169867331e+29*cos(theta)**3 + 1.26813892026795e+27*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl31_m19(theta, phi):
    return 3.97384923581397e-28*(1.0 - cos(theta)**2)**9.5*(3.72055539826978e+33*cos(theta)**12 - 4.02551895550501e+33*cos(theta)**10 + 1.53515553387903e+33*cos(theta)**8 - 2.51370496775514e+32*cos(theta)**6 + 1.71388975074214e+31*cos(theta)**4 - 3.88050509601994e+29*cos(theta)**2 + 1.26813892026795e+27)*cos(19*phi)

#@torch.jit.script
def Yl31_m20(theta, phi):
    return 1.60633334701383e-29*(1.0 - cos(theta)**2)**10*(4.46466647792374e+34*cos(theta)**11 - 4.02551895550501e+34*cos(theta)**9 + 1.22812442710322e+34*cos(theta)**7 - 1.50822298065308e+33*cos(theta)**5 + 6.85555900296855e+31*cos(theta)**3 - 7.76101019203987e+29*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl31_m21(theta, phi):
    return 6.7164171342413e-31*(1.0 - cos(theta)**2)**10.5*(4.91113312571611e+35*cos(theta)**10 - 3.62296705995451e+35*cos(theta)**8 + 8.59687098972257e+34*cos(theta)**6 - 7.54111490326541e+33*cos(theta)**4 + 2.05666770089057e+32*cos(theta)**2 - 7.76101019203987e+29)*cos(21*phi)

#@torch.jit.script
def Yl31_m22(theta, phi):
    return 2.9174251739327e-32*(1.0 - cos(theta)**2)**11*(4.91113312571611e+36*cos(theta)**9 - 2.89837364796361e+36*cos(theta)**7 + 5.15812259383354e+35*cos(theta)**5 - 3.01644596130616e+34*cos(theta)**3 + 4.11333540178113e+32*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl31_m23(theta, phi):
    return 1.32337093312696e-33*(1.0 - cos(theta)**2)**11.5*(4.4200198131445e+37*cos(theta)**8 - 2.02886155357453e+37*cos(theta)**6 + 2.57906129691677e+36*cos(theta)**4 - 9.04933788391849e+34*cos(theta)**2 + 4.11333540178113e+32)*cos(23*phi)

#@torch.jit.script
def Yl31_m24(theta, phi):
    return 6.30892338215793e-35*(1.0 - cos(theta)**2)**12*(3.5360158505156e+38*cos(theta)**7 - 1.21731693214472e+38*cos(theta)**5 + 1.03162451876671e+37*cos(theta)**3 - 1.8098675767837e+35*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl31_m25(theta, phi):
    return 3.18648750393588e-36*(1.0 - cos(theta)**2)**12.5*(2.47521109536092e+39*cos(theta)**6 - 6.08658466072358e+38*cos(theta)**4 + 3.09487355630012e+37*cos(theta)**2 - 1.8098675767837e+35)*cos(25*phi)

#@torch.jit.script
def Yl31_m26(theta, phi):
    return 1.72305510434632e-37*(1.0 - cos(theta)**2)**13*(1.48512665721655e+40*cos(theta)**5 - 2.43463386428943e+39*cos(theta)**3 + 6.18974711260025e+37*cos(theta))*cos(26*phi)

#@torch.jit.script
def Yl31_m27(theta, phi):
    return 1.01181279661018e-38*(1.0 - cos(theta)**2)**13.5*(7.42563328608276e+40*cos(theta)**4 - 7.30390159286829e+39*cos(theta)**2 + 6.18974711260025e+37)*cos(27*phi)

#@torch.jit.script
def Yl31_m28(theta, phi):
    return 6.58634030535703e-40*(1.0 - cos(theta)**2)**14*(2.97025331443311e+41*cos(theta)**3 - 1.46078031857366e+40*cos(theta))*cos(28*phi)

#@torch.jit.script
def Yl31_m29(theta, phi):
    return 4.90916821524168e-41*(1.0 - cos(theta)**2)**14.5*(8.91075994329932e+41*cos(theta)**2 - 1.46078031857366e+40)*cos(29*phi)

#@torch.jit.script
def Yl31_m30(theta, phi):
    return 7.92086730695805*(1.0 - cos(theta)**2)**15*cos(30*phi)*cos(theta)

#@torch.jit.script
def Yl31_m31(theta, phi):
    return 1.00595115393533*(1.0 - cos(theta)**2)**15.5*cos(31*phi)

#@torch.jit.script
def Yl32_m_minus_32(theta, phi):
    return 1.01377968565312*(1.0 - cos(theta)**2)**16*sin(32*phi)

#@torch.jit.script
def Yl32_m_minus_31(theta, phi):
    return 8.11023748522498*(1.0 - cos(theta)**2)**15.5*sin(31*phi)*cos(theta)

#@torch.jit.script
def Yl32_m_minus_30(theta, phi):
    return 8.10836994187712e-43*(1.0 - cos(theta)**2)**15*(5.61377876427857e+43*cos(theta)**2 - 8.91075994329932e+41)*sin(30*phi)

#@torch.jit.script
def Yl32_m_minus_29(theta, phi):
    return 1.10583422533699e-41*(1.0 - cos(theta)**2)**14.5*(1.87125958809286e+43*cos(theta)**3 - 8.91075994329932e+41*cos(theta))*sin(29*phi)

#@torch.jit.script
def Yl32_m_minus_28(theta, phi):
    return 1.72736828000894e-40*(1.0 - cos(theta)**2)**14*(4.67814897023214e+42*cos(theta)**4 - 4.45537997164966e+41*cos(theta)**2 + 3.65195079643415e+39)*sin(28*phi)

#@torch.jit.script
def Yl32_m_minus_27(theta, phi):
    return 2.99188962435835e-39*(1.0 - cos(theta)**2)**13.5*(9.35629794046428e+41*cos(theta)**5 - 1.48512665721655e+41*cos(theta)**3 + 3.65195079643415e+39*cos(theta))*sin(27*phi)

#@torch.jit.script
def Yl32_m_minus_26(theta, phi):
    return 5.62920673595975e-38*(1.0 - cos(theta)**2)**13*(1.55938299007738e+41*cos(theta)**6 - 3.71281664304138e+40*cos(theta)**4 + 1.82597539821707e+39*cos(theta)**2 - 1.03162451876671e+37)*sin(26*phi)

#@torch.jit.script
def Yl32_m_minus_25(theta, phi):
    return 1.13425372828688e-36*(1.0 - cos(theta)**2)**12.5*(2.22768998582483e+40*cos(theta)**7 - 7.42563328608276e+39*cos(theta)**5 + 6.08658466072358e+38*cos(theta)**3 - 1.03162451876671e+37*cos(theta))*sin(25*phi)

#@torch.jit.script
def Yl32_m_minus_24(theta, phi):
    return 2.42210316291546e-35*(1.0 - cos(theta)**2)**12*(2.78461248228104e+39*cos(theta)**8 - 1.23760554768046e+39*cos(theta)**6 + 1.52164616518089e+38*cos(theta)**4 - 5.15812259383354e+36*cos(theta)**2 + 2.26233447097962e+34)*sin(24*phi)

#@torch.jit.script
def Yl32_m_minus_23(theta, phi):
    return 5.43760811463069e-34*(1.0 - cos(theta)**2)**11.5*(3.09401386920115e+38*cos(theta)**9 - 1.7680079252578e+38*cos(theta)**7 + 3.04329233036179e+37*cos(theta)**5 - 1.71937419794451e+36*cos(theta)**3 + 2.26233447097962e+34*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl32_m_minus_22(theta, phi):
    return 1.27523213983038e-32*(1.0 - cos(theta)**2)**11*(3.09401386920115e+37*cos(theta)**10 - 2.21000990657225e+37*cos(theta)**8 + 5.07215388393631e+36*cos(theta)**6 - 4.29843549486128e+35*cos(theta)**4 + 1.13116723548981e+34*cos(theta)**2 - 4.11333540178113e+31)*sin(22*phi)

#@torch.jit.script
def Yl32_m_minus_21(theta, phi):
    return 3.10801046364243e-31*(1.0 - cos(theta)**2)**10.5*(2.81273988109196e+36*cos(theta)**11 - 2.45556656285806e+36*cos(theta)**9 + 7.24593411990902e+35*cos(theta)**7 - 8.59687098972257e+34*cos(theta)**5 + 3.7705574516327e+33*cos(theta)**3 - 4.11333540178113e+31*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl32_m_minus_20(theta, phi):
    return 7.83810415265227e-30*(1.0 - cos(theta)**2)**10*(2.34394990090996e+35*cos(theta)**12 - 2.45556656285806e+35*cos(theta)**10 + 9.05741764988628e+34*cos(theta)**8 - 1.43281183162043e+34*cos(theta)**6 + 9.42639362908176e+32*cos(theta)**4 - 2.05666770089057e+31*cos(theta)**2 + 6.46750849336656e+28)*sin(20*phi)

#@torch.jit.script
def Yl32_m_minus_19(theta, phi):
    return 2.03790707968959e-28*(1.0 - cos(theta)**2)**9.5*(1.80303838531536e+34*cos(theta)**13 - 2.23233323896187e+34*cos(theta)**11 + 1.00637973887625e+34*cos(theta)**9 - 2.04687404517204e+33*cos(theta)**7 + 1.88527872581635e+32*cos(theta)**5 - 6.85555900296855e+30*cos(theta)**3 + 6.46750849336656e+28*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl32_m_minus_18(theta, phi):
    return 5.44544635409307e-27*(1.0 - cos(theta)**2)**9*(1.28788456093954e+33*cos(theta)**14 - 1.86027769913489e+33*cos(theta)**12 + 1.00637973887625e+33*cos(theta)**10 - 2.55859255646505e+32*cos(theta)**8 + 3.14213120969392e+31*cos(theta)**6 - 1.71388975074214e+30*cos(theta)**4 + 3.23375424668328e+28*cos(theta)**2 - 9.05813514477109e+25)*sin(18*phi)

#@torch.jit.script
def Yl32_m_minus_17(theta, phi):
    return 1.49129690191052e-25*(1.0 - cos(theta)**2)**8.5*(8.58589707293027e+31*cos(theta)**15 - 1.43098284548838e+32*cos(theta)**13 + 9.14890671705684e+31*cos(theta)**11 - 2.8428806182945e+31*cos(theta)**9 + 4.48875887099132e+30*cos(theta)**7 - 3.42777950148428e+29*cos(theta)**5 + 1.07791808222776e+28*cos(theta)**3 - 9.05813514477109e+25*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl32_m_minus_16(theta, phi):
    return 4.17563132534946e-24*(1.0 - cos(theta)**2)**8*(5.36618567058142e+30*cos(theta)**16 - 1.02213060392027e+31*cos(theta)**14 + 7.6240889308807e+30*cos(theta)**12 - 2.8428806182945e+30*cos(theta)**10 + 5.61094858873914e+29*cos(theta)**8 - 5.71296583580713e+28*cos(theta)**6 + 2.6947952055694e+27*cos(theta)**4 - 4.52906757238555e+25*cos(theta)**2 + 1.1553743807106e+23)*sin(16*phi)

#@torch.jit.script
def Yl32_m_minus_15(theta, phi):
    return 1.19279889015859e-22*(1.0 - cos(theta)**2)**7.5*(3.15657980622436e+29*cos(theta)**17 - 6.81420402613513e+29*cos(theta)**15 + 5.86468379298516e+29*cos(theta)**13 - 2.58443692572227e+29*cos(theta)**11 + 6.23438732082127e+28*cos(theta)**9 - 8.16137976543875e+27*cos(theta)**7 + 5.3895904111388e+26*cos(theta)**5 - 1.50968919079518e+25*cos(theta)**3 + 1.1553743807106e+23*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl32_m_minus_14(theta, phi):
    return 3.4693842922622e-21*(1.0 - cos(theta)**2)**7*(1.75365544790242e+28*cos(theta)**18 - 4.25887751633446e+28*cos(theta)**16 + 4.18905985213225e+28*cos(theta)**14 - 2.15369743810189e+28*cos(theta)**12 + 6.23438732082127e+27*cos(theta)**10 - 1.02017247067984e+27*cos(theta)**8 + 8.98265068523133e+25*cos(theta)**6 - 3.77422297698796e+24*cos(theta)**4 + 5.77687190355299e+22*cos(theta)**2 - 1.36569075734113e+20)*sin(14*phi)

#@torch.jit.script
def Yl32_m_minus_13(theta, phi):
    return 1.02567111293552e-19*(1.0 - cos(theta)**2)**6.5*(9.22976551527592e+26*cos(theta)**19 - 2.50522206843203e+27*cos(theta)**17 + 2.79270656808817e+27*cos(theta)**15 - 1.65669033700146e+27*cos(theta)**13 + 5.66762483711025e+26*cos(theta)**11 - 1.13352496742205e+26*cos(theta)**9 + 1.2832358121759e+25*cos(theta)**7 - 7.54844595397591e+23*cos(theta)**5 + 1.925623967851e+22*cos(theta)**3 - 1.36569075734113e+20*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl32_m_minus_12(theta, phi):
    return 3.07701333880655e-18*(1.0 - cos(theta)**2)**6*(4.61488275763796e+25*cos(theta)**20 - 1.3917900380178e+26*cos(theta)**18 + 1.74544160505511e+26*cos(theta)**16 - 1.18335024071533e+26*cos(theta)**14 + 4.72302069759187e+25*cos(theta)**12 - 1.13352496742205e+25*cos(theta)**10 + 1.60404476521988e+24*cos(theta)**8 - 1.25807432566265e+23*cos(theta)**6 + 4.81405991962749e+21*cos(theta)**4 - 6.82845378670567e+19*cos(theta)**2 + 1.51743417482348e+17)*sin(12*phi)

#@torch.jit.script
def Yl32_m_minus_11(theta, phi):
    return 9.35331077456894e-17*(1.0 - cos(theta)**2)**5.5*(2.19756321792284e+24*cos(theta)**21 - 7.32521072640946e+24*cos(theta)**19 + 1.02673035591477e+25*cos(theta)**17 - 7.88900160476884e+24*cos(theta)**15 + 3.63309284430144e+24*cos(theta)**13 - 1.03047724311095e+24*cos(theta)**11 + 1.78227196135542e+23*cos(theta)**9 - 1.79724903666093e+22*cos(theta)**7 + 9.62811983925499e+20*cos(theta)**5 - 2.27615126223522e+19*cos(theta)**3 + 1.51743417482348e+17*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl32_m_minus_10(theta, phi):
    return 2.87680836403125e-15*(1.0 - cos(theta)**2)**5*(9.98892371783108e+22*cos(theta)**22 - 3.66260536320473e+23*cos(theta)**20 + 5.70405753285982e+23*cos(theta)**18 - 4.93062600298053e+23*cos(theta)**16 + 2.59506631735817e+23*cos(theta)**14 - 8.58731035925795e+22*cos(theta)**12 + 1.78227196135542e+22*cos(theta)**10 - 2.24656129582616e+21*cos(theta)**8 + 1.60468663987583e+20*cos(theta)**6 - 5.69037815558805e+18*cos(theta)**4 + 7.58717087411741e+16*cos(theta)**2 - 160405303892546.0)*sin(10*phi)

#@torch.jit.script
def Yl32_m_minus_9(theta, phi):
    return 8.9412758972117e-14*(1.0 - cos(theta)**2)**4.5*(4.34301031210047e+21*cos(theta)**23 - 1.74409779200225e+22*cos(theta)**21 + 3.00213554361043e+22*cos(theta)**19 - 2.90036823704737e+22*cos(theta)**17 + 1.73004421157211e+22*cos(theta)**15 - 6.60562335327535e+21*cos(theta)**13 + 1.62024723759584e+21*cos(theta)**11 - 2.49617921758463e+20*cos(theta)**9 + 2.2924094855369e+19*cos(theta)**7 - 1.13807563111761e+18*cos(theta)**5 + 2.52905695803914e+16*cos(theta)**3 - 160405303892546.0*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl32_m_minus_8(theta, phi):
    return 2.80476865419125e-12*(1.0 - cos(theta)**2)**4*(1.80958763004186e+20*cos(theta)**24 - 7.92771723637387e+20*cos(theta)**22 + 1.50106777180522e+21*cos(theta)**20 - 1.61131568724854e+21*cos(theta)**18 + 1.08127763223257e+21*cos(theta)**16 - 4.71830239519668e+20*cos(theta)**14 + 1.35020603132987e+20*cos(theta)**12 - 2.49617921758463e+19*cos(theta)**10 + 2.86551185692113e+18*cos(theta)**8 - 1.89679271852935e+17*cos(theta)**6 + 6.32264239509784e+15*cos(theta)**4 - 80202651946272.8*cos(theta)**2 + 163013520216.002)*sin(8*phi)

#@torch.jit.script
def Yl32_m_minus_7(theta, phi):
    return 8.86945725708952e-11*(1.0 - cos(theta)**2)**3.5*(7.23835052016745e+18*cos(theta)**25 - 3.44683358103212e+19*cos(theta)**23 + 7.14794177050103e+19*cos(theta)**21 - 8.48060888025546e+19*cos(theta)**19 + 6.3604566601916e+19*cos(theta)**17 - 3.14553493013112e+19*cos(theta)**15 + 1.0386200240999e+19*cos(theta)**13 - 2.26925383416784e+18*cos(theta)**11 + 3.1839020632457e+17*cos(theta)**9 - 2.70970388361336e+16*cos(theta)**7 + 1.26452847901957e+15*cos(theta)**5 - 26734217315424.3*cos(theta)**3 + 163013520216.002*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl32_m_minus_6(theta, phi):
    return 2.8243337947883e-9*(1.0 - cos(theta)**2)**3*(2.78398096929517e+17*cos(theta)**26 - 1.43618065876338e+18*cos(theta)**24 + 3.24906444113683e+18*cos(theta)**22 - 4.24030444012773e+18*cos(theta)**20 + 3.53358703343978e+18*cos(theta)**18 - 1.96595933133195e+18*cos(theta)**16 + 7.41871445785641e+17*cos(theta)**14 - 1.89104486180654e+17*cos(theta)**12 + 3.1839020632457e+16*cos(theta)**10 - 3.3871298545167e+15*cos(theta)**8 + 210754746503261.0*cos(theta)**6 - 6683554328856.07*cos(theta)**4 + 81506760108.0008*cos(theta)**2 - 160762840.449706)*sin(6*phi)

#@torch.jit.script
def Yl32_m_minus_5(theta, phi):
    return 9.04668988104336e-8*(1.0 - cos(theta)**2)**2.5*(1.03110406270192e+16*cos(theta)**27 - 5.74472263505353e+16*cos(theta)**25 + 1.41263671353775e+17*cos(theta)**23 - 2.01919259053701e+17*cos(theta)**21 + 1.85978264917883e+17*cos(theta)**19 - 1.15644666548938e+17*cos(theta)**17 + 4.94580963857094e+16*cos(theta)**15 - 1.45464989369733e+16*cos(theta)**13 + 2.89445642113245e+15*cos(theta)**11 - 376347761612967.0*cos(theta)**9 + 30107820929037.3*cos(theta)**7 - 1336710865771.21*cos(theta)**5 + 27168920036.0003*cos(theta)**3 - 160762840.449706*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl32_m_minus_4(theta, phi):
    return 2.91185389957512e-6*(1.0 - cos(theta)**2)**2*(368251450964970.0*cos(theta)**28 - 2.20950870578982e+15*cos(theta)**26 + 5.88598630640731e+15*cos(theta)**24 - 9.17814813880461e+15*cos(theta)**22 + 9.29891324589415e+15*cos(theta)**20 - 6.42470369716323e+15*cos(theta)**18 + 3.09113102410684e+15*cos(theta)**16 - 1.03903563835524e+15*cos(theta)**14 + 241204701761038.0*cos(theta)**12 - 37634776161296.7*cos(theta)**10 + 3763477616129.67*cos(theta)**8 - 222785144295.202*cos(theta)**6 + 6792230009.00007*cos(theta)**4 - 80381420.2248529*cos(theta)**2 + 155176.486920565)*sin(4*phi)

#@torch.jit.script
def Yl32_m_minus_3(theta, phi):
    return 9.40848788610558e-5*(1.0 - cos(theta)**2)**1.5*(12698325895343.8*cos(theta)**29 - 81833655769993.3*cos(theta)**27 + 235439452256292.0*cos(theta)**25 - 399049919078461.0*cos(theta)**23 + 442805392661626.0*cos(theta)**21 - 338142299850696.0*cos(theta)**19 + 181831236712167.0*cos(theta)**17 - 69269042557015.9*cos(theta)**15 + 18554207827772.1*cos(theta)**13 - 3421343287390.6*cos(theta)**11 + 418164179569.963*cos(theta)**9 - 31826449185.0289*cos(theta)**7 + 1358446001.80001*cos(theta)**5 - 26793806.7416176*cos(theta)**3 + 155176.486920565*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl32_m_minus_2(theta, phi):
    return 0.00304869851769809*(1.0 - cos(theta)**2)*(423277529844.793*cos(theta)**30 - 2922630563214.05*cos(theta)**28 + 9055363548318.93*cos(theta)**26 - 16627079961602.6*cos(theta)**24 + 20127517848255.7*cos(theta)**22 - 16907114992534.8*cos(theta)**20 + 10101735372898.2*cos(theta)**18 - 4329315159813.5*cos(theta)**16 + 1325300559126.58*cos(theta)**14 - 285111940615.884*cos(theta)**12 + 41816417956.9963*cos(theta)**10 - 3978306148.12861*cos(theta)**8 + 226407666.966669*cos(theta)**6 - 6698451.6854044*cos(theta)**4 + 77588.2434602827*cos(theta)**2 - 147.787130400538)*sin(2*phi)

#@torch.jit.script
def Yl32_m_minus_1(theta, phi):
    return 0.0989771136930781*(1.0 - cos(theta)**2)**0.5*(13654113865.9611*cos(theta)**31 - 100780364248.76*cos(theta)**29 + 335383835122.923*cos(theta)**27 - 665083198464.102*cos(theta)**25 + 875109471663.293*cos(theta)**23 - 805100713930.229*cos(theta)**21 + 531670282784.114*cos(theta)**19 - 254665597636.088*cos(theta)**17 + 88353370608.4387*cos(theta)**15 - 21931687739.6834*cos(theta)**13 + 3801492541.54512*cos(theta)**11 - 442034016.458735*cos(theta)**9 + 32343952.4238098*cos(theta)**7 - 1339690.33708088*cos(theta)**5 + 25862.7478200942*cos(theta)**3 - 147.787130400538*cos(theta))*sin(phi)

#@torch.jit.script
def Yl32_m0(theta, phi):
    return 3048703300.55346*cos(theta)**32 - 24002489477.3733*cos(theta)**30 + 85582646907.0276*cos(theta)**28 - 182769720513.313*cos(theta)**26 + 260527013889.591*cos(theta)**24 - 261474384849.19*cos(theta)**22 + 189938939937.619*cos(theta)**20 - 101087951227.304*cos(theta)**18 + 39455246269.8407*cos(theta)**16 - 11192977665.203*cos(theta)**14 + 2263468816.74106*cos(theta)**12 - 315832858.149915*cos(theta)**10 + 28887151.6600532*cos(theta)**8 - 1595345.65380964*cos(theta)**6 + 46197.2679674607*cos(theta)**4 - 527.96877677098*cos(theta)**2 + 0.999940865096552

#@torch.jit.script
def Yl32_m1(theta, phi):
    return 0.0989771136930781*(1.0 - cos(theta)**2)**0.5*(13654113865.9611*cos(theta)**31 - 100780364248.76*cos(theta)**29 + 335383835122.923*cos(theta)**27 - 665083198464.102*cos(theta)**25 + 875109471663.293*cos(theta)**23 - 805100713930.229*cos(theta)**21 + 531670282784.114*cos(theta)**19 - 254665597636.088*cos(theta)**17 + 88353370608.4387*cos(theta)**15 - 21931687739.6834*cos(theta)**13 + 3801492541.54512*cos(theta)**11 - 442034016.458735*cos(theta)**9 + 32343952.4238098*cos(theta)**7 - 1339690.33708088*cos(theta)**5 + 25862.7478200942*cos(theta)**3 - 147.787130400538*cos(theta))*cos(phi)

#@torch.jit.script
def Yl32_m2(theta, phi):
    return 0.00304869851769809*(1.0 - cos(theta)**2)*(423277529844.793*cos(theta)**30 - 2922630563214.05*cos(theta)**28 + 9055363548318.93*cos(theta)**26 - 16627079961602.6*cos(theta)**24 + 20127517848255.7*cos(theta)**22 - 16907114992534.8*cos(theta)**20 + 10101735372898.2*cos(theta)**18 - 4329315159813.5*cos(theta)**16 + 1325300559126.58*cos(theta)**14 - 285111940615.884*cos(theta)**12 + 41816417956.9963*cos(theta)**10 - 3978306148.12861*cos(theta)**8 + 226407666.966669*cos(theta)**6 - 6698451.6854044*cos(theta)**4 + 77588.2434602827*cos(theta)**2 - 147.787130400538)*cos(2*phi)

#@torch.jit.script
def Yl32_m3(theta, phi):
    return 9.40848788610558e-5*(1.0 - cos(theta)**2)**1.5*(12698325895343.8*cos(theta)**29 - 81833655769993.3*cos(theta)**27 + 235439452256292.0*cos(theta)**25 - 399049919078461.0*cos(theta)**23 + 442805392661626.0*cos(theta)**21 - 338142299850696.0*cos(theta)**19 + 181831236712167.0*cos(theta)**17 - 69269042557015.9*cos(theta)**15 + 18554207827772.1*cos(theta)**13 - 3421343287390.6*cos(theta)**11 + 418164179569.963*cos(theta)**9 - 31826449185.0289*cos(theta)**7 + 1358446001.80001*cos(theta)**5 - 26793806.7416176*cos(theta)**3 + 155176.486920565*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl32_m4(theta, phi):
    return 2.91185389957512e-6*(1.0 - cos(theta)**2)**2*(368251450964970.0*cos(theta)**28 - 2.20950870578982e+15*cos(theta)**26 + 5.88598630640731e+15*cos(theta)**24 - 9.17814813880461e+15*cos(theta)**22 + 9.29891324589415e+15*cos(theta)**20 - 6.42470369716323e+15*cos(theta)**18 + 3.09113102410684e+15*cos(theta)**16 - 1.03903563835524e+15*cos(theta)**14 + 241204701761038.0*cos(theta)**12 - 37634776161296.7*cos(theta)**10 + 3763477616129.67*cos(theta)**8 - 222785144295.202*cos(theta)**6 + 6792230009.00007*cos(theta)**4 - 80381420.2248529*cos(theta)**2 + 155176.486920565)*cos(4*phi)

#@torch.jit.script
def Yl32_m5(theta, phi):
    return 9.04668988104336e-8*(1.0 - cos(theta)**2)**2.5*(1.03110406270192e+16*cos(theta)**27 - 5.74472263505353e+16*cos(theta)**25 + 1.41263671353775e+17*cos(theta)**23 - 2.01919259053701e+17*cos(theta)**21 + 1.85978264917883e+17*cos(theta)**19 - 1.15644666548938e+17*cos(theta)**17 + 4.94580963857094e+16*cos(theta)**15 - 1.45464989369733e+16*cos(theta)**13 + 2.89445642113245e+15*cos(theta)**11 - 376347761612967.0*cos(theta)**9 + 30107820929037.3*cos(theta)**7 - 1336710865771.21*cos(theta)**5 + 27168920036.0003*cos(theta)**3 - 160762840.449706*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl32_m6(theta, phi):
    return 2.8243337947883e-9*(1.0 - cos(theta)**2)**3*(2.78398096929517e+17*cos(theta)**26 - 1.43618065876338e+18*cos(theta)**24 + 3.24906444113683e+18*cos(theta)**22 - 4.24030444012773e+18*cos(theta)**20 + 3.53358703343978e+18*cos(theta)**18 - 1.96595933133195e+18*cos(theta)**16 + 7.41871445785641e+17*cos(theta)**14 - 1.89104486180654e+17*cos(theta)**12 + 3.1839020632457e+16*cos(theta)**10 - 3.3871298545167e+15*cos(theta)**8 + 210754746503261.0*cos(theta)**6 - 6683554328856.07*cos(theta)**4 + 81506760108.0008*cos(theta)**2 - 160762840.449706)*cos(6*phi)

#@torch.jit.script
def Yl32_m7(theta, phi):
    return 8.86945725708952e-11*(1.0 - cos(theta)**2)**3.5*(7.23835052016745e+18*cos(theta)**25 - 3.44683358103212e+19*cos(theta)**23 + 7.14794177050103e+19*cos(theta)**21 - 8.48060888025546e+19*cos(theta)**19 + 6.3604566601916e+19*cos(theta)**17 - 3.14553493013112e+19*cos(theta)**15 + 1.0386200240999e+19*cos(theta)**13 - 2.26925383416784e+18*cos(theta)**11 + 3.1839020632457e+17*cos(theta)**9 - 2.70970388361336e+16*cos(theta)**7 + 1.26452847901957e+15*cos(theta)**5 - 26734217315424.3*cos(theta)**3 + 163013520216.002*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl32_m8(theta, phi):
    return 2.80476865419125e-12*(1.0 - cos(theta)**2)**4*(1.80958763004186e+20*cos(theta)**24 - 7.92771723637387e+20*cos(theta)**22 + 1.50106777180522e+21*cos(theta)**20 - 1.61131568724854e+21*cos(theta)**18 + 1.08127763223257e+21*cos(theta)**16 - 4.71830239519668e+20*cos(theta)**14 + 1.35020603132987e+20*cos(theta)**12 - 2.49617921758463e+19*cos(theta)**10 + 2.86551185692113e+18*cos(theta)**8 - 1.89679271852935e+17*cos(theta)**6 + 6.32264239509784e+15*cos(theta)**4 - 80202651946272.8*cos(theta)**2 + 163013520216.002)*cos(8*phi)

#@torch.jit.script
def Yl32_m9(theta, phi):
    return 8.9412758972117e-14*(1.0 - cos(theta)**2)**4.5*(4.34301031210047e+21*cos(theta)**23 - 1.74409779200225e+22*cos(theta)**21 + 3.00213554361043e+22*cos(theta)**19 - 2.90036823704737e+22*cos(theta)**17 + 1.73004421157211e+22*cos(theta)**15 - 6.60562335327535e+21*cos(theta)**13 + 1.62024723759584e+21*cos(theta)**11 - 2.49617921758463e+20*cos(theta)**9 + 2.2924094855369e+19*cos(theta)**7 - 1.13807563111761e+18*cos(theta)**5 + 2.52905695803914e+16*cos(theta)**3 - 160405303892546.0*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl32_m10(theta, phi):
    return 2.87680836403125e-15*(1.0 - cos(theta)**2)**5*(9.98892371783108e+22*cos(theta)**22 - 3.66260536320473e+23*cos(theta)**20 + 5.70405753285982e+23*cos(theta)**18 - 4.93062600298053e+23*cos(theta)**16 + 2.59506631735817e+23*cos(theta)**14 - 8.58731035925795e+22*cos(theta)**12 + 1.78227196135542e+22*cos(theta)**10 - 2.24656129582616e+21*cos(theta)**8 + 1.60468663987583e+20*cos(theta)**6 - 5.69037815558805e+18*cos(theta)**4 + 7.58717087411741e+16*cos(theta)**2 - 160405303892546.0)*cos(10*phi)

#@torch.jit.script
def Yl32_m11(theta, phi):
    return 9.35331077456894e-17*(1.0 - cos(theta)**2)**5.5*(2.19756321792284e+24*cos(theta)**21 - 7.32521072640946e+24*cos(theta)**19 + 1.02673035591477e+25*cos(theta)**17 - 7.88900160476884e+24*cos(theta)**15 + 3.63309284430144e+24*cos(theta)**13 - 1.03047724311095e+24*cos(theta)**11 + 1.78227196135542e+23*cos(theta)**9 - 1.79724903666093e+22*cos(theta)**7 + 9.62811983925499e+20*cos(theta)**5 - 2.27615126223522e+19*cos(theta)**3 + 1.51743417482348e+17*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl32_m12(theta, phi):
    return 3.07701333880655e-18*(1.0 - cos(theta)**2)**6*(4.61488275763796e+25*cos(theta)**20 - 1.3917900380178e+26*cos(theta)**18 + 1.74544160505511e+26*cos(theta)**16 - 1.18335024071533e+26*cos(theta)**14 + 4.72302069759187e+25*cos(theta)**12 - 1.13352496742205e+25*cos(theta)**10 + 1.60404476521988e+24*cos(theta)**8 - 1.25807432566265e+23*cos(theta)**6 + 4.81405991962749e+21*cos(theta)**4 - 6.82845378670567e+19*cos(theta)**2 + 1.51743417482348e+17)*cos(12*phi)

#@torch.jit.script
def Yl32_m13(theta, phi):
    return 1.02567111293552e-19*(1.0 - cos(theta)**2)**6.5*(9.22976551527592e+26*cos(theta)**19 - 2.50522206843203e+27*cos(theta)**17 + 2.79270656808817e+27*cos(theta)**15 - 1.65669033700146e+27*cos(theta)**13 + 5.66762483711025e+26*cos(theta)**11 - 1.13352496742205e+26*cos(theta)**9 + 1.2832358121759e+25*cos(theta)**7 - 7.54844595397591e+23*cos(theta)**5 + 1.925623967851e+22*cos(theta)**3 - 1.36569075734113e+20*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl32_m14(theta, phi):
    return 3.4693842922622e-21*(1.0 - cos(theta)**2)**7*(1.75365544790242e+28*cos(theta)**18 - 4.25887751633446e+28*cos(theta)**16 + 4.18905985213225e+28*cos(theta)**14 - 2.15369743810189e+28*cos(theta)**12 + 6.23438732082127e+27*cos(theta)**10 - 1.02017247067984e+27*cos(theta)**8 + 8.98265068523133e+25*cos(theta)**6 - 3.77422297698796e+24*cos(theta)**4 + 5.77687190355299e+22*cos(theta)**2 - 1.36569075734113e+20)*cos(14*phi)

#@torch.jit.script
def Yl32_m15(theta, phi):
    return 1.19279889015859e-22*(1.0 - cos(theta)**2)**7.5*(3.15657980622436e+29*cos(theta)**17 - 6.81420402613513e+29*cos(theta)**15 + 5.86468379298516e+29*cos(theta)**13 - 2.58443692572227e+29*cos(theta)**11 + 6.23438732082127e+28*cos(theta)**9 - 8.16137976543875e+27*cos(theta)**7 + 5.3895904111388e+26*cos(theta)**5 - 1.50968919079518e+25*cos(theta)**3 + 1.1553743807106e+23*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl32_m16(theta, phi):
    return 4.17563132534946e-24*(1.0 - cos(theta)**2)**8*(5.36618567058142e+30*cos(theta)**16 - 1.02213060392027e+31*cos(theta)**14 + 7.6240889308807e+30*cos(theta)**12 - 2.8428806182945e+30*cos(theta)**10 + 5.61094858873914e+29*cos(theta)**8 - 5.71296583580713e+28*cos(theta)**6 + 2.6947952055694e+27*cos(theta)**4 - 4.52906757238555e+25*cos(theta)**2 + 1.1553743807106e+23)*cos(16*phi)

#@torch.jit.script
def Yl32_m17(theta, phi):
    return 1.49129690191052e-25*(1.0 - cos(theta)**2)**8.5*(8.58589707293027e+31*cos(theta)**15 - 1.43098284548838e+32*cos(theta)**13 + 9.14890671705684e+31*cos(theta)**11 - 2.8428806182945e+31*cos(theta)**9 + 4.48875887099132e+30*cos(theta)**7 - 3.42777950148428e+29*cos(theta)**5 + 1.07791808222776e+28*cos(theta)**3 - 9.05813514477109e+25*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl32_m18(theta, phi):
    return 5.44544635409307e-27*(1.0 - cos(theta)**2)**9*(1.28788456093954e+33*cos(theta)**14 - 1.86027769913489e+33*cos(theta)**12 + 1.00637973887625e+33*cos(theta)**10 - 2.55859255646505e+32*cos(theta)**8 + 3.14213120969392e+31*cos(theta)**6 - 1.71388975074214e+30*cos(theta)**4 + 3.23375424668328e+28*cos(theta)**2 - 9.05813514477109e+25)*cos(18*phi)

#@torch.jit.script
def Yl32_m19(theta, phi):
    return 2.03790707968959e-28*(1.0 - cos(theta)**2)**9.5*(1.80303838531536e+34*cos(theta)**13 - 2.23233323896187e+34*cos(theta)**11 + 1.00637973887625e+34*cos(theta)**9 - 2.04687404517204e+33*cos(theta)**7 + 1.88527872581635e+32*cos(theta)**5 - 6.85555900296855e+30*cos(theta)**3 + 6.46750849336656e+28*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl32_m20(theta, phi):
    return 7.83810415265227e-30*(1.0 - cos(theta)**2)**10*(2.34394990090996e+35*cos(theta)**12 - 2.45556656285806e+35*cos(theta)**10 + 9.05741764988628e+34*cos(theta)**8 - 1.43281183162043e+34*cos(theta)**6 + 9.42639362908176e+32*cos(theta)**4 - 2.05666770089057e+31*cos(theta)**2 + 6.46750849336656e+28)*cos(20*phi)

#@torch.jit.script
def Yl32_m21(theta, phi):
    return 3.10801046364243e-31*(1.0 - cos(theta)**2)**10.5*(2.81273988109196e+36*cos(theta)**11 - 2.45556656285806e+36*cos(theta)**9 + 7.24593411990902e+35*cos(theta)**7 - 8.59687098972257e+34*cos(theta)**5 + 3.7705574516327e+33*cos(theta)**3 - 4.11333540178113e+31*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl32_m22(theta, phi):
    return 1.27523213983038e-32*(1.0 - cos(theta)**2)**11*(3.09401386920115e+37*cos(theta)**10 - 2.21000990657225e+37*cos(theta)**8 + 5.07215388393631e+36*cos(theta)**6 - 4.29843549486128e+35*cos(theta)**4 + 1.13116723548981e+34*cos(theta)**2 - 4.11333540178113e+31)*cos(22*phi)

#@torch.jit.script
def Yl32_m23(theta, phi):
    return 5.43760811463069e-34*(1.0 - cos(theta)**2)**11.5*(3.09401386920115e+38*cos(theta)**9 - 1.7680079252578e+38*cos(theta)**7 + 3.04329233036179e+37*cos(theta)**5 - 1.71937419794451e+36*cos(theta)**3 + 2.26233447097962e+34*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl32_m24(theta, phi):
    return 2.42210316291546e-35*(1.0 - cos(theta)**2)**12*(2.78461248228104e+39*cos(theta)**8 - 1.23760554768046e+39*cos(theta)**6 + 1.52164616518089e+38*cos(theta)**4 - 5.15812259383354e+36*cos(theta)**2 + 2.26233447097962e+34)*cos(24*phi)

#@torch.jit.script
def Yl32_m25(theta, phi):
    return 1.13425372828688e-36*(1.0 - cos(theta)**2)**12.5*(2.22768998582483e+40*cos(theta)**7 - 7.42563328608276e+39*cos(theta)**5 + 6.08658466072358e+38*cos(theta)**3 - 1.03162451876671e+37*cos(theta))*cos(25*phi)

#@torch.jit.script
def Yl32_m26(theta, phi):
    return 5.62920673595975e-38*(1.0 - cos(theta)**2)**13*(1.55938299007738e+41*cos(theta)**6 - 3.71281664304138e+40*cos(theta)**4 + 1.82597539821707e+39*cos(theta)**2 - 1.03162451876671e+37)*cos(26*phi)

#@torch.jit.script
def Yl32_m27(theta, phi):
    return 2.99188962435835e-39*(1.0 - cos(theta)**2)**13.5*(9.35629794046428e+41*cos(theta)**5 - 1.48512665721655e+41*cos(theta)**3 + 3.65195079643415e+39*cos(theta))*cos(27*phi)

#@torch.jit.script
def Yl32_m28(theta, phi):
    return 1.72736828000894e-40*(1.0 - cos(theta)**2)**14*(4.67814897023214e+42*cos(theta)**4 - 4.45537997164966e+41*cos(theta)**2 + 3.65195079643415e+39)*cos(28*phi)

#@torch.jit.script
def Yl32_m29(theta, phi):
    return 1.10583422533699e-41*(1.0 - cos(theta)**2)**14.5*(1.87125958809286e+43*cos(theta)**3 - 8.91075994329932e+41*cos(theta))*cos(29*phi)

#@torch.jit.script
def Yl32_m30(theta, phi):
    return 8.10836994187712e-43*(1.0 - cos(theta)**2)**15*(5.61377876427857e+43*cos(theta)**2 - 8.91075994329932e+41)*cos(30*phi)

#@torch.jit.script
def Yl32_m31(theta, phi):
    return 8.11023748522498*(1.0 - cos(theta)**2)**15.5*cos(31*phi)*cos(theta)

#@torch.jit.script
def Yl32_m32(theta, phi):
    return 1.01377968565312*(1.0 - cos(theta)**2)**16*cos(32*phi)

#@torch.jit.script
def Yl33_m_minus_33(theta, phi):
    return 1.02143096163768*(1.0 - cos(theta)**2)**16.5*sin(33*phi)

#@torch.jit.script
def Yl33_m_minus_32(theta, phi):
    return 8.29814436002877*(1.0 - cos(theta)**2)**16*sin(32*phi)*cos(theta)

#@torch.jit.script
def Yl33_m_minus_31(theta, phi):
    return 1.29644475885681e-44*(1.0 - cos(theta)**2)**15.5*(3.64895619678107e+45*cos(theta)**2 - 5.61377876427857e+43)*sin(31*phi)

#@torch.jit.script
def Yl33_m_minus_30(theta, phi):
    return 1.7964065532371e-43*(1.0 - cos(theta)**2)**15*(1.21631873226036e+45*cos(theta)**3 - 5.61377876427857e+43*cos(theta))*sin(30*phi)

#@torch.jit.script
def Yl33_m_minus_29(theta, phi):
    return 2.85170699605925e-42*(1.0 - cos(theta)**2)**14.5*(3.04079683065089e+44*cos(theta)**4 - 2.80688938213928e+43*cos(theta)**2 + 2.22768998582483e+41)*sin(29*phi)

#@torch.jit.script
def Yl33_m_minus_28(theta, phi):
    return 5.02094828227271e-41*(1.0 - cos(theta)**2)**14*(6.08159366130178e+43*cos(theta)**5 - 9.35629794046428e+42*cos(theta)**3 + 2.22768998582483e+41*cos(theta))*sin(28*phi)

#@torch.jit.script
def Yl33_m_minus_27(theta, phi):
    return 9.60563965860272e-40*(1.0 - cos(theta)**2)**13.5*(1.0135989435503e+43*cos(theta)**6 - 2.33907448511607e+42*cos(theta)**4 + 1.11384499291241e+41*cos(theta)**2 - 6.08658466072358e+38)*sin(27*phi)

#@torch.jit.script
def Yl33_m_minus_26(theta, phi):
    return 1.96857033314502e-38*(1.0 - cos(theta)**2)**13*(1.44799849078614e+42*cos(theta)**7 - 4.67814897023214e+41*cos(theta)**5 + 3.71281664304138e+40*cos(theta)**3 - 6.08658466072358e+38*cos(theta))*sin(26*phi)

#@torch.jit.script
def Yl33_m_minus_25(theta, phi):
    return 4.27682948208865e-37*(1.0 - cos(theta)**2)**12.5*(1.80999811348267e+41*cos(theta)**8 - 7.7969149503869e+40*cos(theta)**6 + 9.28204160760346e+39*cos(theta)**4 - 3.04329233036179e+38*cos(theta)**2 + 1.28953064845838e+36)*sin(25*phi)

#@torch.jit.script
def Yl33_m_minus_24(theta, phi):
    return 9.77140888441698e-36*(1.0 - cos(theta)**2)**12*(2.01110901498075e+40*cos(theta)**9 - 1.11384499291241e+40*cos(theta)**7 + 1.85640832152069e+39*cos(theta)**5 - 1.01443077678726e+38*cos(theta)**3 + 1.28953064845838e+36*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl33_m_minus_23(theta, phi):
    return 2.33289189642992e-34*(1.0 - cos(theta)**2)**11.5*(2.01110901498075e+39*cos(theta)**10 - 1.39230624114052e+39*cos(theta)**8 + 3.09401386920115e+38*cos(theta)**6 - 2.53607694196816e+37*cos(theta)**4 + 6.44765324229192e+35*cos(theta)**2 - 2.26233447097962e+33)*sin(23*phi)

#@torch.jit.script
def Yl33_m_minus_22(theta, phi):
    return 5.79008541721441e-33*(1.0 - cos(theta)**2)**11*(1.82828092270977e+38*cos(theta)**11 - 1.54700693460058e+38*cos(theta)**9 + 4.4200198131445e+37*cos(theta)**7 - 5.07215388393631e+36*cos(theta)**5 + 2.14921774743064e+35*cos(theta)**3 - 2.26233447097962e+33*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl33_m_minus_21(theta, phi):
    return 1.48749987668913e-31*(1.0 - cos(theta)**2)**10.5*(1.52356743559148e+37*cos(theta)**12 - 1.54700693460058e+37*cos(theta)**10 + 5.52502476643063e+36*cos(theta)**8 - 8.45358980656052e+35*cos(theta)**6 + 5.3730443685766e+34*cos(theta)**4 - 1.13116723548981e+33*cos(theta)**2 + 3.42777950148428e+30)*sin(21*phi)

#@torch.jit.script
def Yl33_m_minus_20(theta, phi):
    return 3.94117295988316e-30*(1.0 - cos(theta)**2)**10*(1.17197495045498e+36*cos(theta)**13 - 1.40636994054598e+36*cos(theta)**11 + 6.13891640714514e+35*cos(theta)**9 - 1.2076556866515e+35*cos(theta)**7 + 1.07460887371532e+34*cos(theta)**5 - 3.7705574516327e+32*cos(theta)**3 + 3.42777950148428e+30*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl33_m_minus_19(theta, phi):
    return 1.0735627820667e-28*(1.0 - cos(theta)**2)**9.5*(8.37124964610701e+34*cos(theta)**14 - 1.17197495045498e+35*cos(theta)**12 + 6.13891640714514e+34*cos(theta)**10 - 1.50956960831438e+34*cos(theta)**8 + 1.79101478952553e+33*cos(theta)**6 - 9.42639362908176e+31*cos(theta)**4 + 1.71388975074214e+30*cos(theta)**2 - 4.61964892383326e+27)*sin(19*phi)

#@torch.jit.script
def Yl33_m_minus_18(theta, phi):
    return 2.99829767816716e-27*(1.0 - cos(theta)**2)**9*(5.58083309740467e+33*cos(theta)**15 - 9.01519192657678e+33*cos(theta)**13 + 5.58083309740467e+33*cos(theta)**11 - 1.67729956479375e+33*cos(theta)**9 + 2.55859255646505e+32*cos(theta)**7 - 1.88527872581635e+31*cos(theta)**5 + 5.71296583580713e+29*cos(theta)**3 - 4.61964892383326e+27*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl33_m_minus_17(theta, phi):
    return 8.56485131043879e-26*(1.0 - cos(theta)**2)**8.5*(3.48802068587792e+32*cos(theta)**16 - 6.4394228046977e+32*cos(theta)**14 + 4.65069424783723e+32*cos(theta)**12 - 1.67729956479375e+32*cos(theta)**10 + 3.19824069558131e+31*cos(theta)**8 - 3.14213120969392e+30*cos(theta)**6 + 1.42824145895178e+29*cos(theta)**4 - 2.30982446191663e+27*cos(theta)**2 + 5.66133446548193e+24)*sin(17*phi)

#@torch.jit.script
def Yl33_m_minus_16(theta, phi):
    return 2.49706179888357e-24*(1.0 - cos(theta)**2)**8*(2.05177687404584e+31*cos(theta)**17 - 4.29294853646513e+31*cos(theta)**15 + 3.57745711372095e+31*cos(theta)**13 - 1.52481778617614e+31*cos(theta)**11 + 3.55360077286812e+30*cos(theta)**9 - 4.48875887099131e+29*cos(theta)**7 + 2.85648291790356e+28*cos(theta)**5 - 7.69941487305543e+26*cos(theta)**3 + 5.66133446548193e+24*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl33_m_minus_15(theta, phi):
    return 7.41589519033628e-23*(1.0 - cos(theta)**2)**7.5*(1.13987604113658e+30*cos(theta)**18 - 2.68309283529071e+30*cos(theta)**16 + 2.55532650980068e+30*cos(theta)**14 - 1.27068148848012e+30*cos(theta)**12 + 3.55360077286812e+29*cos(theta)**10 - 5.61094858873914e+28*cos(theta)**8 + 4.76080486317261e+27*cos(theta)**6 - 1.92485371826386e+26*cos(theta)**4 + 2.83066723274097e+24*cos(theta)**2 - 6.41874655950333e+21)*sin(15*phi)

#@torch.jit.script
def Yl33_m_minus_14(theta, phi):
    return 2.23955123505438e-21*(1.0 - cos(theta)**2)**7*(5.99934758492935e+28*cos(theta)**19 - 1.57828990311218e+29*cos(theta)**17 + 1.70355100653378e+29*cos(theta)**15 - 9.77447298830859e+28*cos(theta)**13 + 3.23054615715284e+28*cos(theta)**11 - 6.23438732082127e+27*cos(theta)**9 + 6.80114980453229e+26*cos(theta)**7 - 3.84970743652771e+25*cos(theta)**5 + 9.43555744246989e+23*cos(theta)**3 - 6.41874655950333e+21*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl33_m_minus_13(theta, phi):
    return 6.86633406583717e-20*(1.0 - cos(theta)**2)**6.5*(2.99967379246467e+27*cos(theta)**20 - 8.76827723951212e+27*cos(theta)**18 + 1.06471937908361e+28*cos(theta)**16 - 6.98176642022042e+27*cos(theta)**14 + 2.69212179762737e+27*cos(theta)**12 - 6.23438732082127e+26*cos(theta)**10 + 8.50143725566537e+25*cos(theta)**8 - 6.41617906087952e+24*cos(theta)**6 + 2.35888936061747e+23*cos(theta)**4 - 3.20937327975166e+21*cos(theta)**2 + 6.82845378670567e+18)*sin(13*phi)

#@torch.jit.script
def Yl33_m_minus_12(theta, phi):
    return 2.13409374265872e-18*(1.0 - cos(theta)**2)**6*(1.42841609164984e+26*cos(theta)**21 - 4.61488275763796e+26*cos(theta)**19 + 6.26305517108009e+26*cos(theta)**17 - 4.65451094681362e+26*cos(theta)**15 + 2.07086292125182e+26*cos(theta)**13 - 5.66762483711025e+25*cos(theta)**11 + 9.44604139518374e+24*cos(theta)**9 - 9.16597008697075e+23*cos(theta)**7 + 4.71777872123494e+22*cos(theta)**5 - 1.06979109325055e+21*cos(theta)**3 + 6.82845378670567e+18*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl33_m_minus_11(theta, phi):
    return 6.71476920037506e-17*(1.0 - cos(theta)**2)**5.5*(6.4928004165902e+24*cos(theta)**22 - 2.30744137881898e+25*cos(theta)**20 + 3.47947509504449e+25*cos(theta)**18 - 2.90906934175851e+25*cos(theta)**16 + 1.47918780089416e+25*cos(theta)**14 - 4.72302069759187e+24*cos(theta)**12 + 9.44604139518374e+23*cos(theta)**10 - 1.14574626087134e+23*cos(theta)**8 + 7.86296453539157e+21*cos(theta)**6 - 2.67447773312639e+20*cos(theta)**4 + 3.41422689335283e+18*cos(theta)**2 - 6.89742806737946e+15)*sin(11*phi)

#@torch.jit.script
def Yl33_m_minus_10(theta, phi):
    return 2.13609884881944e-15*(1.0 - cos(theta)**2)**5*(2.8229567028653e+23*cos(theta)**23 - 1.09878160896142e+24*cos(theta)**21 + 1.83130268160236e+24*cos(theta)**19 - 1.71121725985795e+24*cos(theta)**17 + 9.86125200596105e+23*cos(theta)**15 - 3.63309284430144e+23*cos(theta)**13 + 8.58731035925795e+22*cos(theta)**11 - 1.27305140096816e+22*cos(theta)**9 + 1.12328064791308e+21*cos(theta)**7 - 5.34895546625277e+19*cos(theta)**5 + 1.13807563111761e+18*cos(theta)**3 - 6.89742806737946e+15*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl33_m_minus_9(theta, phi):
    return 6.86216560370661e-14*(1.0 - cos(theta)**2)**4.5*(1.17623195952721e+22*cos(theta)**24 - 4.99446185891554e+22*cos(theta)**22 + 9.15651340801182e+22*cos(theta)**20 - 9.50676255476637e+22*cos(theta)**18 + 6.16328250372566e+22*cos(theta)**16 - 2.59506631735817e+22*cos(theta)**14 + 7.15609196604829e+21*cos(theta)**12 - 1.27305140096816e+21*cos(theta)**10 + 1.40410080989135e+20*cos(theta)**8 - 8.91492577708795e+18*cos(theta)**6 + 2.84518907779403e+17*cos(theta)**4 - 3.44871403368973e+15*cos(theta)**2 + 6683554328856.07)*sin(9*phi)

#@torch.jit.script
def Yl33_m_minus_8(theta, phi):
    return 2.2235957953578e-12*(1.0 - cos(theta)**2)**4*(4.70492783810884e+20*cos(theta)**25 - 2.17150515605023e+21*cos(theta)**23 + 4.36024448000563e+21*cos(theta)**21 - 5.00355923935072e+21*cos(theta)**19 + 3.62546029630921e+21*cos(theta)**17 - 1.73004421157211e+21*cos(theta)**15 + 5.50468612772945e+20*cos(theta)**13 - 1.1573194554256e+20*cos(theta)**11 + 1.56011201099039e+19*cos(theta)**9 - 1.27356082529828e+18*cos(theta)**7 + 5.69037815558805e+16*cos(theta)**5 - 1.14957134456324e+15*cos(theta)**3 + 6683554328856.07*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl33_m_minus_7(theta, phi):
    return 7.25996365443219e-11*(1.0 - cos(theta)**2)**3.5*(1.80958763004186e+19*cos(theta)**26 - 9.04793815020931e+19*cos(theta)**24 + 1.98192930909347e+20*cos(theta)**22 - 2.50177961967536e+20*cos(theta)**20 + 2.01414460906067e+20*cos(theta)**18 - 1.08127763223257e+20*cos(theta)**16 + 3.9319186626639e+19*cos(theta)**14 - 9.64432879521333e+18*cos(theta)**12 + 1.56011201099039e+18*cos(theta)**10 - 1.59195103162285e+17*cos(theta)**8 + 9.48396359264676e+15*cos(theta)**6 - 287392836140811.0*cos(theta)**4 + 3341777164428.03*cos(theta)**2 - 6269750777.53852)*sin(7*phi)

#@torch.jit.script
def Yl33_m_minus_6(theta, phi):
    return 2.38586751612009e-9*(1.0 - cos(theta)**2)**3*(6.70217640756245e+17*cos(theta)**27 - 3.61917526008372e+18*cos(theta)**25 + 8.6170839525803e+18*cos(theta)**23 - 1.19132362841684e+19*cos(theta)**21 + 1.06007611003193e+19*cos(theta)**19 - 6.3604566601916e+18*cos(theta)**17 + 2.6212791084426e+18*cos(theta)**15 - 7.41871445785641e+17*cos(theta)**13 + 1.4182836463549e+17*cos(theta)**11 - 1.76883447958094e+16*cos(theta)**9 + 1.35485194180668e+15*cos(theta)**7 - 57478567228162.2*cos(theta)**5 + 1113925721476.01*cos(theta)**3 - 6269750777.53852*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl33_m_minus_5(theta, phi):
    return 7.8842001969058e-8*(1.0 - cos(theta)**2)**2.5*(2.3936344312723e+16*cos(theta)**28 - 1.39199048464759e+17*cos(theta)**26 + 3.59045164690846e+17*cos(theta)**24 - 5.41510740189472e+17*cos(theta)**22 + 5.30038055015966e+17*cos(theta)**20 - 3.53358703343978e+17*cos(theta)**18 + 1.63829944277662e+17*cos(theta)**16 - 5.29908175561172e+16*cos(theta)**14 + 1.18190303862908e+16*cos(theta)**12 - 1.76883447958094e+15*cos(theta)**10 + 169356492725835.0*cos(theta)**8 - 9579761204693.69*cos(theta)**6 + 278481430369.003*cos(theta)**4 - 3134875388.76926*cos(theta)**2 + 5741530.01606092)*sin(5*phi)

#@torch.jit.script
def Yl33_m_minus_4(theta, phi):
    return 2.61726947876729e-6*(1.0 - cos(theta)**2)**2*(825391183197346.0*cos(theta)**29 - 5.15552031350958e+15*cos(theta)**27 + 1.43618065876338e+16*cos(theta)**25 - 2.35439452256292e+16*cos(theta)**23 + 2.52399073817127e+16*cos(theta)**21 - 1.85978264917883e+16*cos(theta)**19 + 9.63705554574484e+15*cos(theta)**17 - 3.53272117040781e+15*cos(theta)**15 + 909156183560834.0*cos(theta)**13 - 160803134507358.0*cos(theta)**11 + 18817388080648.3*cos(theta)**9 - 1368537314956.24*cos(theta)**7 + 55696286073.8005*cos(theta)**5 - 1044958462.92309*cos(theta)**3 + 5741530.01606092*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl33_m_minus_3(theta, phi):
    return 8.71986838901848e-5*(1.0 - cos(theta)**2)**1.5*(27513039439911.5*cos(theta)**30 - 184125725482485.0*cos(theta)**28 + 552377176447455.0*cos(theta)**26 - 980997717734551.0*cos(theta)**24 + 1.14726851735058e+15*cos(theta)**22 - 929891324589415.0*cos(theta)**20 + 535391974763602.0*cos(theta)**18 - 220795073150488.0*cos(theta)**16 + 64939727397202.4*cos(theta)**14 - 13400261208946.5*cos(theta)**12 + 1881738808064.83*cos(theta)**10 - 171067164369.53*cos(theta)**8 + 9282714345.63342*cos(theta)**6 - 261239615.730772*cos(theta)**4 + 2870765.00803046*cos(theta)**2 - 5172.54956401885)*sin(3*phi)

#@torch.jit.script
def Yl33_m_minus_2(theta, phi):
    return 0.00291301034789671*(1.0 - cos(theta)**2)*(887517401287.469*cos(theta)**31 - 6349162947671.89*cos(theta)**29 + 20458413942498.3*cos(theta)**27 - 39239908709382.0*cos(theta)**25 + 49881239884807.7*cos(theta)**23 - 44280539266162.6*cos(theta)**21 + 28178524987558.0*cos(theta)**19 - 12987945479440.5*cos(theta)**17 + 4329315159813.5*cos(theta)**15 - 1030789323765.12*cos(theta)**13 + 171067164369.53*cos(theta)**11 - 19007462707.7256*cos(theta)**9 + 1326102049.3762*cos(theta)**7 - 52247923.1461544*cos(theta)**5 + 956921.669343486*cos(theta)**3 - 5172.54956401885*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl33_m_minus_1(theta, phi):
    return 0.0974879725986118*(1.0 - cos(theta)**2)**0.5*(27734918790.2334*cos(theta)**32 - 211638764922.396*cos(theta)**30 + 730657640803.512*cos(theta)**28 - 1509227258053.16*cos(theta)**26 + 2078384995200.32*cos(theta)**24 - 2012751784825.57*cos(theta)**22 + 1408926249377.9*cos(theta)**20 - 721552526635.583*cos(theta)**18 + 270582197488.344*cos(theta)**16 - 73627808840.3656*cos(theta)**14 + 14255597030.7942*cos(theta)**12 - 1900746270.77256*cos(theta)**10 + 165762756.172025*cos(theta)**8 - 8707987.19102573*cos(theta)**6 + 239230.417335872*cos(theta)**4 - 2586.27478200942*cos(theta)**2 + 4.61834782501683)*sin(phi)

#@torch.jit.script
def Yl33_m0(theta, phi):
    return 6096706674.96088*cos(theta)**33 - 49524017298.1438*cos(theta)**31 + 182767206695.531*cos(theta)**29 - 405483529608.663*cos(theta)**27 + 603070842765.427*cos(theta)**25 - 634811413437.292*cos(theta)**23 + 486688750301.924*cos(theta)**21 - 275484198284.108*cos(theta)**19 + 115460288986.722*cos(theta)**17 - 35606801138.7622*cos(theta)**15 + 7954710892.7022*cos(theta)**13 - 1253469595.21368*cos(theta)**11 + 133606255.303784*cos(theta)**9 - 9024062.27192536*cos(theta)**7 + 347079.318150975*cos(theta)**5 - 6253.68140812568*cos(theta)**3 + 33.5018646863876*cos(theta)

#@torch.jit.script
def Yl33_m1(theta, phi):
    return 0.0974879725986118*(1.0 - cos(theta)**2)**0.5*(27734918790.2334*cos(theta)**32 - 211638764922.396*cos(theta)**30 + 730657640803.512*cos(theta)**28 - 1509227258053.16*cos(theta)**26 + 2078384995200.32*cos(theta)**24 - 2012751784825.57*cos(theta)**22 + 1408926249377.9*cos(theta)**20 - 721552526635.583*cos(theta)**18 + 270582197488.344*cos(theta)**16 - 73627808840.3656*cos(theta)**14 + 14255597030.7942*cos(theta)**12 - 1900746270.77256*cos(theta)**10 + 165762756.172025*cos(theta)**8 - 8707987.19102573*cos(theta)**6 + 239230.417335872*cos(theta)**4 - 2586.27478200942*cos(theta)**2 + 4.61834782501683)*cos(phi)

#@torch.jit.script
def Yl33_m2(theta, phi):
    return 0.00291301034789671*(1.0 - cos(theta)**2)*(887517401287.469*cos(theta)**31 - 6349162947671.89*cos(theta)**29 + 20458413942498.3*cos(theta)**27 - 39239908709382.0*cos(theta)**25 + 49881239884807.7*cos(theta)**23 - 44280539266162.6*cos(theta)**21 + 28178524987558.0*cos(theta)**19 - 12987945479440.5*cos(theta)**17 + 4329315159813.5*cos(theta)**15 - 1030789323765.12*cos(theta)**13 + 171067164369.53*cos(theta)**11 - 19007462707.7256*cos(theta)**9 + 1326102049.3762*cos(theta)**7 - 52247923.1461544*cos(theta)**5 + 956921.669343486*cos(theta)**3 - 5172.54956401885*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl33_m3(theta, phi):
    return 8.71986838901848e-5*(1.0 - cos(theta)**2)**1.5*(27513039439911.5*cos(theta)**30 - 184125725482485.0*cos(theta)**28 + 552377176447455.0*cos(theta)**26 - 980997717734551.0*cos(theta)**24 + 1.14726851735058e+15*cos(theta)**22 - 929891324589415.0*cos(theta)**20 + 535391974763602.0*cos(theta)**18 - 220795073150488.0*cos(theta)**16 + 64939727397202.4*cos(theta)**14 - 13400261208946.5*cos(theta)**12 + 1881738808064.83*cos(theta)**10 - 171067164369.53*cos(theta)**8 + 9282714345.63342*cos(theta)**6 - 261239615.730772*cos(theta)**4 + 2870765.00803046*cos(theta)**2 - 5172.54956401885)*cos(3*phi)

#@torch.jit.script
def Yl33_m4(theta, phi):
    return 2.61726947876729e-6*(1.0 - cos(theta)**2)**2*(825391183197346.0*cos(theta)**29 - 5.15552031350958e+15*cos(theta)**27 + 1.43618065876338e+16*cos(theta)**25 - 2.35439452256292e+16*cos(theta)**23 + 2.52399073817127e+16*cos(theta)**21 - 1.85978264917883e+16*cos(theta)**19 + 9.63705554574484e+15*cos(theta)**17 - 3.53272117040781e+15*cos(theta)**15 + 909156183560834.0*cos(theta)**13 - 160803134507358.0*cos(theta)**11 + 18817388080648.3*cos(theta)**9 - 1368537314956.24*cos(theta)**7 + 55696286073.8005*cos(theta)**5 - 1044958462.92309*cos(theta)**3 + 5741530.01606092*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl33_m5(theta, phi):
    return 7.8842001969058e-8*(1.0 - cos(theta)**2)**2.5*(2.3936344312723e+16*cos(theta)**28 - 1.39199048464759e+17*cos(theta)**26 + 3.59045164690846e+17*cos(theta)**24 - 5.41510740189472e+17*cos(theta)**22 + 5.30038055015966e+17*cos(theta)**20 - 3.53358703343978e+17*cos(theta)**18 + 1.63829944277662e+17*cos(theta)**16 - 5.29908175561172e+16*cos(theta)**14 + 1.18190303862908e+16*cos(theta)**12 - 1.76883447958094e+15*cos(theta)**10 + 169356492725835.0*cos(theta)**8 - 9579761204693.69*cos(theta)**6 + 278481430369.003*cos(theta)**4 - 3134875388.76926*cos(theta)**2 + 5741530.01606092)*cos(5*phi)

#@torch.jit.script
def Yl33_m6(theta, phi):
    return 2.38586751612009e-9*(1.0 - cos(theta)**2)**3*(6.70217640756245e+17*cos(theta)**27 - 3.61917526008372e+18*cos(theta)**25 + 8.6170839525803e+18*cos(theta)**23 - 1.19132362841684e+19*cos(theta)**21 + 1.06007611003193e+19*cos(theta)**19 - 6.3604566601916e+18*cos(theta)**17 + 2.6212791084426e+18*cos(theta)**15 - 7.41871445785641e+17*cos(theta)**13 + 1.4182836463549e+17*cos(theta)**11 - 1.76883447958094e+16*cos(theta)**9 + 1.35485194180668e+15*cos(theta)**7 - 57478567228162.2*cos(theta)**5 + 1113925721476.01*cos(theta)**3 - 6269750777.53852*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl33_m7(theta, phi):
    return 7.25996365443219e-11*(1.0 - cos(theta)**2)**3.5*(1.80958763004186e+19*cos(theta)**26 - 9.04793815020931e+19*cos(theta)**24 + 1.98192930909347e+20*cos(theta)**22 - 2.50177961967536e+20*cos(theta)**20 + 2.01414460906067e+20*cos(theta)**18 - 1.08127763223257e+20*cos(theta)**16 + 3.9319186626639e+19*cos(theta)**14 - 9.64432879521333e+18*cos(theta)**12 + 1.56011201099039e+18*cos(theta)**10 - 1.59195103162285e+17*cos(theta)**8 + 9.48396359264676e+15*cos(theta)**6 - 287392836140811.0*cos(theta)**4 + 3341777164428.03*cos(theta)**2 - 6269750777.53852)*cos(7*phi)

#@torch.jit.script
def Yl33_m8(theta, phi):
    return 2.2235957953578e-12*(1.0 - cos(theta)**2)**4*(4.70492783810884e+20*cos(theta)**25 - 2.17150515605023e+21*cos(theta)**23 + 4.36024448000563e+21*cos(theta)**21 - 5.00355923935072e+21*cos(theta)**19 + 3.62546029630921e+21*cos(theta)**17 - 1.73004421157211e+21*cos(theta)**15 + 5.50468612772945e+20*cos(theta)**13 - 1.1573194554256e+20*cos(theta)**11 + 1.56011201099039e+19*cos(theta)**9 - 1.27356082529828e+18*cos(theta)**7 + 5.69037815558805e+16*cos(theta)**5 - 1.14957134456324e+15*cos(theta)**3 + 6683554328856.07*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl33_m9(theta, phi):
    return 6.86216560370661e-14*(1.0 - cos(theta)**2)**4.5*(1.17623195952721e+22*cos(theta)**24 - 4.99446185891554e+22*cos(theta)**22 + 9.15651340801182e+22*cos(theta)**20 - 9.50676255476637e+22*cos(theta)**18 + 6.16328250372566e+22*cos(theta)**16 - 2.59506631735817e+22*cos(theta)**14 + 7.15609196604829e+21*cos(theta)**12 - 1.27305140096816e+21*cos(theta)**10 + 1.40410080989135e+20*cos(theta)**8 - 8.91492577708795e+18*cos(theta)**6 + 2.84518907779403e+17*cos(theta)**4 - 3.44871403368973e+15*cos(theta)**2 + 6683554328856.07)*cos(9*phi)

#@torch.jit.script
def Yl33_m10(theta, phi):
    return 2.13609884881944e-15*(1.0 - cos(theta)**2)**5*(2.8229567028653e+23*cos(theta)**23 - 1.09878160896142e+24*cos(theta)**21 + 1.83130268160236e+24*cos(theta)**19 - 1.71121725985795e+24*cos(theta)**17 + 9.86125200596105e+23*cos(theta)**15 - 3.63309284430144e+23*cos(theta)**13 + 8.58731035925795e+22*cos(theta)**11 - 1.27305140096816e+22*cos(theta)**9 + 1.12328064791308e+21*cos(theta)**7 - 5.34895546625277e+19*cos(theta)**5 + 1.13807563111761e+18*cos(theta)**3 - 6.89742806737946e+15*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl33_m11(theta, phi):
    return 6.71476920037506e-17*(1.0 - cos(theta)**2)**5.5*(6.4928004165902e+24*cos(theta)**22 - 2.30744137881898e+25*cos(theta)**20 + 3.47947509504449e+25*cos(theta)**18 - 2.90906934175851e+25*cos(theta)**16 + 1.47918780089416e+25*cos(theta)**14 - 4.72302069759187e+24*cos(theta)**12 + 9.44604139518374e+23*cos(theta)**10 - 1.14574626087134e+23*cos(theta)**8 + 7.86296453539157e+21*cos(theta)**6 - 2.67447773312639e+20*cos(theta)**4 + 3.41422689335283e+18*cos(theta)**2 - 6.89742806737946e+15)*cos(11*phi)

#@torch.jit.script
def Yl33_m12(theta, phi):
    return 2.13409374265872e-18*(1.0 - cos(theta)**2)**6*(1.42841609164984e+26*cos(theta)**21 - 4.61488275763796e+26*cos(theta)**19 + 6.26305517108009e+26*cos(theta)**17 - 4.65451094681362e+26*cos(theta)**15 + 2.07086292125182e+26*cos(theta)**13 - 5.66762483711025e+25*cos(theta)**11 + 9.44604139518374e+24*cos(theta)**9 - 9.16597008697075e+23*cos(theta)**7 + 4.71777872123494e+22*cos(theta)**5 - 1.06979109325055e+21*cos(theta)**3 + 6.82845378670567e+18*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl33_m13(theta, phi):
    return 6.86633406583717e-20*(1.0 - cos(theta)**2)**6.5*(2.99967379246467e+27*cos(theta)**20 - 8.76827723951212e+27*cos(theta)**18 + 1.06471937908361e+28*cos(theta)**16 - 6.98176642022042e+27*cos(theta)**14 + 2.69212179762737e+27*cos(theta)**12 - 6.23438732082127e+26*cos(theta)**10 + 8.50143725566537e+25*cos(theta)**8 - 6.41617906087952e+24*cos(theta)**6 + 2.35888936061747e+23*cos(theta)**4 - 3.20937327975166e+21*cos(theta)**2 + 6.82845378670567e+18)*cos(13*phi)

#@torch.jit.script
def Yl33_m14(theta, phi):
    return 2.23955123505438e-21*(1.0 - cos(theta)**2)**7*(5.99934758492935e+28*cos(theta)**19 - 1.57828990311218e+29*cos(theta)**17 + 1.70355100653378e+29*cos(theta)**15 - 9.77447298830859e+28*cos(theta)**13 + 3.23054615715284e+28*cos(theta)**11 - 6.23438732082127e+27*cos(theta)**9 + 6.80114980453229e+26*cos(theta)**7 - 3.84970743652771e+25*cos(theta)**5 + 9.43555744246989e+23*cos(theta)**3 - 6.41874655950333e+21*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl33_m15(theta, phi):
    return 7.41589519033628e-23*(1.0 - cos(theta)**2)**7.5*(1.13987604113658e+30*cos(theta)**18 - 2.68309283529071e+30*cos(theta)**16 + 2.55532650980068e+30*cos(theta)**14 - 1.27068148848012e+30*cos(theta)**12 + 3.55360077286812e+29*cos(theta)**10 - 5.61094858873914e+28*cos(theta)**8 + 4.76080486317261e+27*cos(theta)**6 - 1.92485371826386e+26*cos(theta)**4 + 2.83066723274097e+24*cos(theta)**2 - 6.41874655950333e+21)*cos(15*phi)

#@torch.jit.script
def Yl33_m16(theta, phi):
    return 2.49706179888357e-24*(1.0 - cos(theta)**2)**8*(2.05177687404584e+31*cos(theta)**17 - 4.29294853646513e+31*cos(theta)**15 + 3.57745711372095e+31*cos(theta)**13 - 1.52481778617614e+31*cos(theta)**11 + 3.55360077286812e+30*cos(theta)**9 - 4.48875887099131e+29*cos(theta)**7 + 2.85648291790356e+28*cos(theta)**5 - 7.69941487305543e+26*cos(theta)**3 + 5.66133446548193e+24*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl33_m17(theta, phi):
    return 8.56485131043879e-26*(1.0 - cos(theta)**2)**8.5*(3.48802068587792e+32*cos(theta)**16 - 6.4394228046977e+32*cos(theta)**14 + 4.65069424783723e+32*cos(theta)**12 - 1.67729956479375e+32*cos(theta)**10 + 3.19824069558131e+31*cos(theta)**8 - 3.14213120969392e+30*cos(theta)**6 + 1.42824145895178e+29*cos(theta)**4 - 2.30982446191663e+27*cos(theta)**2 + 5.66133446548193e+24)*cos(17*phi)

#@torch.jit.script
def Yl33_m18(theta, phi):
    return 2.99829767816716e-27*(1.0 - cos(theta)**2)**9*(5.58083309740467e+33*cos(theta)**15 - 9.01519192657678e+33*cos(theta)**13 + 5.58083309740467e+33*cos(theta)**11 - 1.67729956479375e+33*cos(theta)**9 + 2.55859255646505e+32*cos(theta)**7 - 1.88527872581635e+31*cos(theta)**5 + 5.71296583580713e+29*cos(theta)**3 - 4.61964892383326e+27*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl33_m19(theta, phi):
    return 1.0735627820667e-28*(1.0 - cos(theta)**2)**9.5*(8.37124964610701e+34*cos(theta)**14 - 1.17197495045498e+35*cos(theta)**12 + 6.13891640714514e+34*cos(theta)**10 - 1.50956960831438e+34*cos(theta)**8 + 1.79101478952553e+33*cos(theta)**6 - 9.42639362908176e+31*cos(theta)**4 + 1.71388975074214e+30*cos(theta)**2 - 4.61964892383326e+27)*cos(19*phi)

#@torch.jit.script
def Yl33_m20(theta, phi):
    return 3.94117295988316e-30*(1.0 - cos(theta)**2)**10*(1.17197495045498e+36*cos(theta)**13 - 1.40636994054598e+36*cos(theta)**11 + 6.13891640714514e+35*cos(theta)**9 - 1.2076556866515e+35*cos(theta)**7 + 1.07460887371532e+34*cos(theta)**5 - 3.7705574516327e+32*cos(theta)**3 + 3.42777950148428e+30*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl33_m21(theta, phi):
    return 1.48749987668913e-31*(1.0 - cos(theta)**2)**10.5*(1.52356743559148e+37*cos(theta)**12 - 1.54700693460058e+37*cos(theta)**10 + 5.52502476643063e+36*cos(theta)**8 - 8.45358980656052e+35*cos(theta)**6 + 5.3730443685766e+34*cos(theta)**4 - 1.13116723548981e+33*cos(theta)**2 + 3.42777950148428e+30)*cos(21*phi)

#@torch.jit.script
def Yl33_m22(theta, phi):
    return 5.79008541721441e-33*(1.0 - cos(theta)**2)**11*(1.82828092270977e+38*cos(theta)**11 - 1.54700693460058e+38*cos(theta)**9 + 4.4200198131445e+37*cos(theta)**7 - 5.07215388393631e+36*cos(theta)**5 + 2.14921774743064e+35*cos(theta)**3 - 2.26233447097962e+33*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl33_m23(theta, phi):
    return 2.33289189642992e-34*(1.0 - cos(theta)**2)**11.5*(2.01110901498075e+39*cos(theta)**10 - 1.39230624114052e+39*cos(theta)**8 + 3.09401386920115e+38*cos(theta)**6 - 2.53607694196816e+37*cos(theta)**4 + 6.44765324229192e+35*cos(theta)**2 - 2.26233447097962e+33)*cos(23*phi)

#@torch.jit.script
def Yl33_m24(theta, phi):
    return 9.77140888441698e-36*(1.0 - cos(theta)**2)**12*(2.01110901498075e+40*cos(theta)**9 - 1.11384499291241e+40*cos(theta)**7 + 1.85640832152069e+39*cos(theta)**5 - 1.01443077678726e+38*cos(theta)**3 + 1.28953064845838e+36*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl33_m25(theta, phi):
    return 4.27682948208865e-37*(1.0 - cos(theta)**2)**12.5*(1.80999811348267e+41*cos(theta)**8 - 7.7969149503869e+40*cos(theta)**6 + 9.28204160760346e+39*cos(theta)**4 - 3.04329233036179e+38*cos(theta)**2 + 1.28953064845838e+36)*cos(25*phi)

#@torch.jit.script
def Yl33_m26(theta, phi):
    return 1.96857033314502e-38*(1.0 - cos(theta)**2)**13*(1.44799849078614e+42*cos(theta)**7 - 4.67814897023214e+41*cos(theta)**5 + 3.71281664304138e+40*cos(theta)**3 - 6.08658466072358e+38*cos(theta))*cos(26*phi)

#@torch.jit.script
def Yl33_m27(theta, phi):
    return 9.60563965860272e-40*(1.0 - cos(theta)**2)**13.5*(1.0135989435503e+43*cos(theta)**6 - 2.33907448511607e+42*cos(theta)**4 + 1.11384499291241e+41*cos(theta)**2 - 6.08658466072358e+38)*cos(27*phi)

#@torch.jit.script
def Yl33_m28(theta, phi):
    return 5.02094828227271e-41*(1.0 - cos(theta)**2)**14*(6.08159366130178e+43*cos(theta)**5 - 9.35629794046428e+42*cos(theta)**3 + 2.22768998582483e+41*cos(theta))*cos(28*phi)

#@torch.jit.script
def Yl33_m29(theta, phi):
    return 2.85170699605925e-42*(1.0 - cos(theta)**2)**14.5*(3.04079683065089e+44*cos(theta)**4 - 2.80688938213928e+43*cos(theta)**2 + 2.22768998582483e+41)*cos(29*phi)

#@torch.jit.script
def Yl33_m30(theta, phi):
    return 1.7964065532371e-43*(1.0 - cos(theta)**2)**15*(1.21631873226036e+45*cos(theta)**3 - 5.61377876427857e+43*cos(theta))*cos(30*phi)

#@torch.jit.script
def Yl33_m31(theta, phi):
    return 1.29644475885681e-44*(1.0 - cos(theta)**2)**15.5*(3.64895619678107e+45*cos(theta)**2 - 5.61377876427857e+43)*cos(31*phi)

#@torch.jit.script
def Yl33_m32(theta, phi):
    return 8.29814436002877*(1.0 - cos(theta)**2)**16*cos(32*phi)*cos(theta)

#@torch.jit.script
def Yl33_m33(theta, phi):
    return 1.02143096163768*(1.0 - cos(theta)**2)**16.5*cos(33*phi)

#@torch.jit.script
def Yl34_m_minus_34(theta, phi):
    return 1.0289140723859*(1.0 - cos(theta)**2)**17*sin(34*phi)

#@torch.jit.script
def Yl34_m_minus_33(theta, phi):
    return 8.48464280026292*(1.0 - cos(theta)**2)**16.5*sin(33*phi)*cos(theta)

#@torch.jit.script
def Yl34_m_minus_32(theta, phi):
    return 2.0086881349656e-46*(1.0 - cos(theta)**2)**16*(2.44480065184332e+47*cos(theta)**2 - 3.64895619678107e+45)*sin(32*phi)

#@torch.jit.script
def Yl34_m_minus_31(theta, phi):
    return 2.8264747454439e-45*(1.0 - cos(theta)**2)**15.5*(8.14933550614439e+46*cos(theta)**3 - 3.64895619678107e+45*cos(theta))*sin(31*phi)

#@torch.jit.script
def Yl34_m_minus_30(theta, phi):
    return 4.55755358336505e-44*(1.0 - cos(theta)**2)**15*(2.0373338765361e+46*cos(theta)**4 - 1.82447809839054e+45*cos(theta)**2 + 1.40344469106964e+43)*sin(30*phi)

#@torch.jit.script
def Yl34_m_minus_29(theta, phi):
    return 8.15279969880161e-43*(1.0 - cos(theta)**2)**14.5*(4.0746677530722e+45*cos(theta)**5 - 6.08159366130178e+44*cos(theta)**3 + 1.40344469106964e+43*cos(theta))*sin(29*phi)

#@torch.jit.script
def Yl34_m_minus_28(theta, phi):
    return 1.58508542441973e-41*(1.0 - cos(theta)**2)**14*(6.79111292178699e+44*cos(theta)**6 - 1.52039841532545e+44*cos(theta)**4 + 7.01722345534821e+42*cos(theta)**2 - 3.71281664304138e+40)*sin(28*phi)

#@torch.jit.script
def Yl34_m_minus_27(theta, phi):
    return 3.30215562682199e-40*(1.0 - cos(theta)**2)**13.5*(9.70158988826713e+43*cos(theta)**7 - 3.04079683065089e+43*cos(theta)**5 + 2.33907448511607e+42*cos(theta)**3 - 3.71281664304138e+40*cos(theta))*sin(27*phi)

#@torch.jit.script
def Yl34_m_minus_26(theta, phi):
    return 7.29470020663704e-39*(1.0 - cos(theta)**2)**13*(1.21269873603339e+43*cos(theta)**8 - 5.06799471775149e+42*cos(theta)**6 + 5.84768621279018e+41*cos(theta)**4 - 1.85640832152069e+40*cos(theta)**2 + 7.60823082590447e+37)*sin(26*phi)

#@torch.jit.script
def Yl34_m_minus_25(theta, phi):
    return 1.69513514495286e-37*(1.0 - cos(theta)**2)**12.5*(1.3474430400371e+42*cos(theta)**9 - 7.23999245393069e+41*cos(theta)**7 + 1.16953724255804e+41*cos(theta)**5 - 6.1880277384023e+39*cos(theta)**3 + 7.60823082590447e+37*cos(theta))*sin(25*phi)

#@torch.jit.script
def Yl34_m_minus_24(theta, phi):
    return 4.11746896065541e-36*(1.0 - cos(theta)**2)**12*(1.3474430400371e+41*cos(theta)**10 - 9.04999056741337e+40*cos(theta)**8 + 1.94922873759673e+40*cos(theta)**6 - 1.54700693460058e+39*cos(theta)**4 + 3.80411541295224e+37*cos(theta)**2 - 1.28953064845838e+35)*sin(24*phi)

#@torch.jit.script
def Yl34_m_minus_23(theta, phi):
    return 1.04001756281185e-34*(1.0 - cos(theta)**2)**11.5*(1.22494821821555e+40*cos(theta)**11 - 1.00555450749037e+40*cos(theta)**9 + 2.78461248228104e+39*cos(theta)**7 - 3.09401386920115e+38*cos(theta)**5 + 1.26803847098408e+37*cos(theta)**3 - 1.28953064845838e+35*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl34_m_minus_22(theta, phi):
    return 2.71999887348259e-33*(1.0 - cos(theta)**2)**11*(1.02079018184629e+39*cos(theta)**12 - 1.00555450749037e+39*cos(theta)**10 + 3.4807656028513e+38*cos(theta)**8 - 5.15668978200192e+37*cos(theta)**6 + 3.1700961774602e+36*cos(theta)**4 - 6.44765324229192e+34*cos(theta)**2 + 1.88527872581635e+32)*sin(22*phi)

#@torch.jit.script
def Yl34_m_minus_21(theta, phi):
    return 7.33895819488808e-32*(1.0 - cos(theta)**2)**10.5*(7.85223216804838e+37*cos(theta)**13 - 9.14140461354886e+37*cos(theta)**11 + 3.86751733650144e+37*cos(theta)**9 - 7.36669968857417e+36*cos(theta)**7 + 6.34019235492039e+35*cos(theta)**5 - 2.14921774743064e+34*cos(theta)**3 + 1.88527872581635e+32*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl34_m_minus_20(theta, phi):
    return 2.03647825147882e-30*(1.0 - cos(theta)**2)**10*(5.6087372628917e+36*cos(theta)**14 - 7.61783717795738e+36*cos(theta)**12 + 3.86751733650144e+36*cos(theta)**10 - 9.20837461071771e+35*cos(theta)**8 + 1.05669872582007e+35*cos(theta)**6 - 5.3730443685766e+33*cos(theta)**4 + 9.42639362908176e+31*cos(theta)**2 - 2.44841392963163e+29)*sin(20*phi)

#@torch.jit.script
def Yl34_m_minus_19(theta, phi):
    return 5.79591871206322e-29*(1.0 - cos(theta)**2)**9.5*(3.73915817526113e+35*cos(theta)**15 - 5.85987475227491e+35*cos(theta)**13 + 3.51592485136495e+35*cos(theta)**11 - 1.02315273452419e+35*cos(theta)**9 + 1.50956960831438e+34*cos(theta)**7 - 1.07460887371532e+33*cos(theta)**5 + 3.14213120969392e+31*cos(theta)**3 - 2.44841392963163e+29*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl34_m_minus_18(theta, phi):
    return 1.6877970053263e-27*(1.0 - cos(theta)**2)**9*(2.33697385953821e+34*cos(theta)**16 - 4.18562482305351e+34*cos(theta)**14 + 2.92993737613745e+34*cos(theta)**12 - 1.02315273452419e+34*cos(theta)**10 + 1.88696201039297e+33*cos(theta)**8 - 1.79101478952553e+32*cos(theta)**6 + 7.8553280242348e+30*cos(theta)**4 - 1.22420696481581e+29*cos(theta)**2 + 2.88728057739579e+26)*sin(18*phi)

#@torch.jit.script
def Yl34_m_minus_17(theta, phi):
    return 5.01818126253981e-26*(1.0 - cos(theta)**2)**8.5*(1.37469050561071e+33*cos(theta)**17 - 2.79041654870234e+33*cos(theta)**15 + 2.2537979816442e+33*cos(theta)**13 - 9.30138849567446e+32*cos(theta)**11 + 2.09662445599219e+32*cos(theta)**9 - 2.55859255646505e+31*cos(theta)**7 + 1.57106560484696e+30*cos(theta)**5 - 4.08068988271938e+28*cos(theta)**3 + 2.88728057739579e+26*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl34_m_minus_16(theta, phi):
    return 1.52043439327851e-24*(1.0 - cos(theta)**2)**8*(7.63716947561506e+31*cos(theta)**18 - 1.74401034293896e+32*cos(theta)**16 + 1.60985570117443e+32*cos(theta)**14 - 7.75115707972871e+31*cos(theta)**12 + 2.09662445599219e+31*cos(theta)**10 - 3.19824069558131e+30*cos(theta)**8 + 2.61844267474493e+29*cos(theta)**6 - 1.02017247067984e+28*cos(theta)**4 + 1.44364028869789e+26*cos(theta)**2 - 3.14518581415663e+23)*sin(16*phi)

#@torch.jit.script
def Yl34_m_minus_15(theta, phi):
    return 4.68629353226083e-23*(1.0 - cos(theta)**2)**7.5*(4.01956288190266e+30*cos(theta)**19 - 1.02588843702292e+31*cos(theta)**17 + 1.07323713411628e+31*cos(theta)**15 - 5.96242852286824e+30*cos(theta)**13 + 1.90602223272018e+30*cos(theta)**11 - 3.55360077286812e+29*cos(theta)**9 + 3.74063239249276e+28*cos(theta)**7 - 2.04034494135969e+27*cos(theta)**5 + 4.81213429565964e+25*cos(theta)**3 - 3.14518581415663e+23*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl34_m_minus_14(theta, phi):
    return 1.46704192609139e-21*(1.0 - cos(theta)**2)**7*(2.00978144095133e+29*cos(theta)**20 - 5.69938020568288e+29*cos(theta)**18 + 6.70773208822677e+29*cos(theta)**16 - 4.25887751633446e+29*cos(theta)**14 + 1.58835186060015e+29*cos(theta)**12 - 3.55360077286812e+28*cos(theta)**10 + 4.67579049061595e+27*cos(theta)**8 - 3.40057490226615e+26*cos(theta)**6 + 1.20303357391491e+25*cos(theta)**4 - 1.57259290707831e+23*cos(theta)**2 + 3.20937327975166e+20)*sin(14*phi)

#@torch.jit.script
def Yl34_m_minus_13(theta, phi):
    return 4.65771371921163e-20*(1.0 - cos(theta)**2)**6.5*(9.57038781405396e+27*cos(theta)**21 - 2.99967379246467e+28*cos(theta)**19 + 3.94572475778045e+28*cos(theta)**17 - 2.83925167755631e+28*cos(theta)**15 + 1.22180912353857e+28*cos(theta)**13 - 3.23054615715284e+27*cos(theta)**11 + 5.19532276735106e+26*cos(theta)**9 - 4.8579641460945e+25*cos(theta)**7 + 2.40606714782982e+24*cos(theta)**5 - 5.24197635692772e+22*cos(theta)**3 + 3.20937327975166e+20*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl34_m_minus_12(theta, phi):
    return 1.49772838629695e-18*(1.0 - cos(theta)**2)**6*(4.35017627911543e+26*cos(theta)**22 - 1.49983689623234e+27*cos(theta)**20 + 2.19206930987803e+27*cos(theta)**18 - 1.77453229847269e+27*cos(theta)**16 + 8.72720802527553e+26*cos(theta)**14 - 2.69212179762737e+26*cos(theta)**12 + 5.19532276735106e+25*cos(theta)**10 - 6.07245518261812e+24*cos(theta)**8 + 4.0101119130497e+23*cos(theta)**6 - 1.31049408923193e+22*cos(theta)**4 + 1.60468663987583e+20*cos(theta)**2 - 3.10384263032076e+17)*sin(12*phi)

#@torch.jit.script
def Yl34_m_minus_11(theta, phi):
    return 4.87164793230034e-17*(1.0 - cos(theta)**2)**5.5*(1.89138099091975e+25*cos(theta)**23 - 7.14208045824922e+25*cos(theta)**21 + 1.15372068940949e+26*cos(theta)**19 - 1.04384252851335e+26*cos(theta)**17 + 5.81813868351702e+25*cos(theta)**15 - 2.07086292125182e+25*cos(theta)**13 + 4.72302069759187e+24*cos(theta)**11 - 6.74717242513125e+23*cos(theta)**9 + 5.72873130435672e+22*cos(theta)**7 - 2.62098817846386e+21*cos(theta)**5 + 5.34895546625277e+19*cos(theta)**3 - 3.10384263032076e+17*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl34_m_minus_10(theta, phi):
    return 1.60098687884658e-15*(1.0 - cos(theta)**2)**5*(7.88075412883231e+23*cos(theta)**24 - 3.2464002082951e+24*cos(theta)**22 + 5.76860344704745e+24*cos(theta)**20 - 5.79912515840749e+24*cos(theta)**18 + 3.63633667719814e+24*cos(theta)**16 - 1.47918780089416e+24*cos(theta)**14 + 3.93585058132656e+23*cos(theta)**12 - 6.74717242513125e+22*cos(theta)**10 + 7.1609141304459e+21*cos(theta)**8 - 4.3683136307731e+20*cos(theta)**6 + 1.33723886656319e+19*cos(theta)**4 - 1.55192131516038e+17*cos(theta)**2 + 287392836140811.0)*sin(10*phi)

#@torch.jit.script
def Yl34_m_minus_9(theta, phi):
    return 5.30987277141628e-14*(1.0 - cos(theta)**2)**4.5*(3.15230165153292e+22*cos(theta)**25 - 1.41147835143265e+23*cos(theta)**23 + 2.74695402240355e+23*cos(theta)**21 - 3.05217113600394e+23*cos(theta)**19 + 2.13902157482243e+23*cos(theta)**17 - 9.86125200596105e+22*cos(theta)**15 + 3.0275773702512e+22*cos(theta)**13 - 6.13379311375568e+21*cos(theta)**11 + 7.956571256051e+20*cos(theta)**9 - 6.24044804396157e+19*cos(theta)**7 + 2.67447773312639e+18*cos(theta)**5 - 5.17307105053459e+16*cos(theta)**3 + 287392836140811.0*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl34_m_minus_8(theta, phi):
    return 1.77543598061902e-12*(1.0 - cos(theta)**2)**4*(1.21242371212805e+21*cos(theta)**26 - 5.88115979763605e+21*cos(theta)**24 + 1.24861546472888e+22*cos(theta)**22 - 1.52608556800197e+22*cos(theta)**20 + 1.1883453193458e+22*cos(theta)**18 - 6.16328250372566e+21*cos(theta)**16 + 2.16255526446514e+21*cos(theta)**14 - 5.11149426146306e+20*cos(theta)**12 + 7.956571256051e+19*cos(theta)**10 - 7.80056005495196e+18*cos(theta)**8 + 4.45746288854398e+17*cos(theta)**6 - 1.29326776263365e+16*cos(theta)**4 + 143696418070405.0*cos(theta)**2 - 257059781879.079)*sin(8*phi)

#@torch.jit.script
def Yl34_m_minus_7(theta, phi):
    return 5.97876583646464e-11*(1.0 - cos(theta)**2)**3.5*(4.49045819306684e+19*cos(theta)**27 - 2.35246391905442e+20*cos(theta)**25 + 5.42876289012559e+20*cos(theta)**23 - 7.26707413334272e+20*cos(theta)**21 + 6.2544490491884e+20*cos(theta)**19 - 3.62546029630921e+20*cos(theta)**17 + 1.44170350964343e+20*cos(theta)**15 - 3.9319186626639e+19*cos(theta)**13 + 7.23324659641e+18*cos(theta)**11 - 8.66728894994662e+17*cos(theta)**9 + 6.36780412649139e+16*cos(theta)**7 - 2.5865355252673e+15*cos(theta)**5 + 47898806023468.5*cos(theta)**3 - 257059781879.079*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl34_m_minus_6(theta, phi):
    return 2.0257343306691e-9*(1.0 - cos(theta)**2)**3*(1.60373506895244e+18*cos(theta)**28 - 9.04793815020931e+18*cos(theta)**26 + 2.26198453755233e+19*cos(theta)**24 - 3.30321551515578e+19*cos(theta)**22 + 3.1272245245942e+19*cos(theta)**20 - 2.01414460906067e+19*cos(theta)**18 + 9.01064693527143e+18*cos(theta)**16 - 2.80851333047421e+18*cos(theta)**14 + 6.02770549700833e+17*cos(theta)**12 - 8.66728894994662e+16*cos(theta)**10 + 7.95975515811424e+15*cos(theta)**8 - 431089254211216.0*cos(theta)**6 + 11974701505867.1*cos(theta)**4 - 128529890939.54*cos(theta)**2 + 223919670.626376)*sin(6*phi)

#@torch.jit.script
def Yl34_m_minus_5(theta, phi):
    return 6.89940251833707e-8*(1.0 - cos(theta)**2)**2.5*(5.53012092742222e+16*cos(theta)**29 - 3.35108820378123e+17*cos(theta)**27 + 9.04793815020931e+17*cos(theta)**25 - 1.43618065876338e+18*cos(theta)**23 + 1.48915453552105e+18*cos(theta)**21 - 1.06007611003193e+18*cos(theta)**19 + 5.30038055015966e+17*cos(theta)**17 - 1.87234222031614e+17*cos(theta)**15 + 4.63669653616025e+16*cos(theta)**13 - 7.87935359086056e+15*cos(theta)**11 + 884417239790471.0*cos(theta)**9 - 61584179173030.9*cos(theta)**7 + 2394940301173.42*cos(theta)**5 - 42843296979.8466*cos(theta)**3 + 223919670.626376*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl34_m_minus_4(theta, phi):
    return 2.35995875978251e-6*(1.0 - cos(theta)**2)**2*(1.84337364247407e+15*cos(theta)**30 - 1.19681721563615e+16*cos(theta)**28 + 3.47997621161897e+16*cos(theta)**26 - 5.98408607818076e+16*cos(theta)**24 + 6.7688842523684e+16*cos(theta)**22 - 5.30038055015966e+16*cos(theta)**20 + 2.94465586119981e+16*cos(theta)**18 - 1.17021388769759e+16*cos(theta)**16 + 3.31192609725732e+15*cos(theta)**14 - 656612799238380.0*cos(theta)**12 + 88441723979047.1*cos(theta)**10 - 7698022396628.86*cos(theta)**8 + 399156716862.237*cos(theta)**6 - 10710824244.9616*cos(theta)**4 + 111959835.313188*cos(theta)**2 - 191384.333868697)*sin(4*phi)

#@torch.jit.script
def Yl34_m_minus_3(theta, phi):
    return 8.09985154172335e-5*(1.0 - cos(theta)**2)**1.5*(59463665886260.4*cos(theta)**31 - 412695591598673.0*cos(theta)**29 + 1.28888007837739e+15*cos(theta)**27 - 2.3936344312723e+15*cos(theta)**25 + 2.94299315320365e+15*cos(theta)**23 - 2.52399073817127e+15*cos(theta)**21 + 1.54981887431569e+15*cos(theta)**19 - 688361110410346.0*cos(theta)**17 + 220795073150488.0*cos(theta)**15 - 50508676864490.8*cos(theta)**13 + 8040156725367.92*cos(theta)**11 - 855335821847.651*cos(theta)**9 + 57022388123.1768*cos(theta)**7 - 2142164848.99233*cos(theta)**5 + 37319945.104396*cos(theta)**3 - 191384.333868697*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl34_m_minus_2(theta, phi):
    return 0.00278710230306644*(1.0 - cos(theta)**2)*(1858239558945.64*cos(theta)**32 - 13756519719955.8*cos(theta)**30 + 46031431370621.2*cos(theta)**28 - 92062862741242.5*cos(theta)**26 + 122624714716819.0*cos(theta)**24 - 114726851735058.0*cos(theta)**22 + 77490943715784.6*cos(theta)**20 - 38242283911685.9*cos(theta)**18 + 13799692071905.5*cos(theta)**16 - 3607762633177.91*cos(theta)**14 + 670013060447.327*cos(theta)**12 - 85533582184.7651*cos(theta)**10 + 7127798515.39709*cos(theta)**8 - 357027474.832055*cos(theta)**6 + 9329986.27609899*cos(theta)**4 - 95692.1669343486*cos(theta)**2 + 161.642173875589)*sin(2*phi)

#@torch.jit.script
def Yl34_m_minus_1(theta, phi):
    return 0.0960641026936534*(1.0 - cos(theta)**2)**0.5*(56310289665.0193*cos(theta)**33 - 443758700643.735*cos(theta)**31 + 1587290736917.97*cos(theta)**29 - 3409735657083.05*cos(theta)**27 + 4904988588672.75*cos(theta)**25 - 4988123988480.77*cos(theta)**23 + 3690044938846.88*cos(theta)**21 - 2012751784825.57*cos(theta)**19 + 811746592465.031*cos(theta)**17 - 240517508878.528*cos(theta)**15 + 51539466188.2559*cos(theta)**13 - 7775780198.61501*cos(theta)**11 + 791977612.821899*cos(theta)**9 - 51003924.9760078*cos(theta)**7 + 1865997.2552198*cos(theta)**5 - 31897.3889781162*cos(theta)**3 + 161.642173875589*cos(theta))*sin(phi)

#@torch.jit.script
def Yl34_m0(theta, phi):
    return 12192094786.7008*cos(theta)**34 - 102086047393.122*cos(theta)**32 + 389497534669.142*cos(theta)**30 - 896462579794.057*cos(theta)**28 + 1388782193287.51*cos(theta)**26 - 1530014280740.48*cos(theta)**24 + 1234748366913.37*cos(theta)**22 - 740849020148.023*cos(theta)**20 + 331984230726.708*cos(theta)**18 - 110661410242.236*cos(theta)**16 + 27100753528.7109*cos(theta)**14 - 4770151975.0729*cos(theta)**12 + 583018574.731132*cos(theta)**10 - 46933516.7493756*cos(theta)**8 + 2289439.84143296*cos(theta)**6 - 58703.5856777681*cos(theta)**4 + 594.968773761163*cos(theta)**2 - 0.999947518926325

#@torch.jit.script
def Yl34_m1(theta, phi):
    return 0.0960641026936534*(1.0 - cos(theta)**2)**0.5*(56310289665.0193*cos(theta)**33 - 443758700643.735*cos(theta)**31 + 1587290736917.97*cos(theta)**29 - 3409735657083.05*cos(theta)**27 + 4904988588672.75*cos(theta)**25 - 4988123988480.77*cos(theta)**23 + 3690044938846.88*cos(theta)**21 - 2012751784825.57*cos(theta)**19 + 811746592465.031*cos(theta)**17 - 240517508878.528*cos(theta)**15 + 51539466188.2559*cos(theta)**13 - 7775780198.61501*cos(theta)**11 + 791977612.821899*cos(theta)**9 - 51003924.9760078*cos(theta)**7 + 1865997.2552198*cos(theta)**5 - 31897.3889781162*cos(theta)**3 + 161.642173875589*cos(theta))*cos(phi)

#@torch.jit.script
def Yl34_m2(theta, phi):
    return 0.00278710230306644*(1.0 - cos(theta)**2)*(1858239558945.64*cos(theta)**32 - 13756519719955.8*cos(theta)**30 + 46031431370621.2*cos(theta)**28 - 92062862741242.5*cos(theta)**26 + 122624714716819.0*cos(theta)**24 - 114726851735058.0*cos(theta)**22 + 77490943715784.6*cos(theta)**20 - 38242283911685.9*cos(theta)**18 + 13799692071905.5*cos(theta)**16 - 3607762633177.91*cos(theta)**14 + 670013060447.327*cos(theta)**12 - 85533582184.7651*cos(theta)**10 + 7127798515.39709*cos(theta)**8 - 357027474.832055*cos(theta)**6 + 9329986.27609899*cos(theta)**4 - 95692.1669343486*cos(theta)**2 + 161.642173875589)*cos(2*phi)

#@torch.jit.script
def Yl34_m3(theta, phi):
    return 8.09985154172335e-5*(1.0 - cos(theta)**2)**1.5*(59463665886260.4*cos(theta)**31 - 412695591598673.0*cos(theta)**29 + 1.28888007837739e+15*cos(theta)**27 - 2.3936344312723e+15*cos(theta)**25 + 2.94299315320365e+15*cos(theta)**23 - 2.52399073817127e+15*cos(theta)**21 + 1.54981887431569e+15*cos(theta)**19 - 688361110410346.0*cos(theta)**17 + 220795073150488.0*cos(theta)**15 - 50508676864490.8*cos(theta)**13 + 8040156725367.92*cos(theta)**11 - 855335821847.651*cos(theta)**9 + 57022388123.1768*cos(theta)**7 - 2142164848.99233*cos(theta)**5 + 37319945.104396*cos(theta)**3 - 191384.333868697*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl34_m4(theta, phi):
    return 2.35995875978251e-6*(1.0 - cos(theta)**2)**2*(1.84337364247407e+15*cos(theta)**30 - 1.19681721563615e+16*cos(theta)**28 + 3.47997621161897e+16*cos(theta)**26 - 5.98408607818076e+16*cos(theta)**24 + 6.7688842523684e+16*cos(theta)**22 - 5.30038055015966e+16*cos(theta)**20 + 2.94465586119981e+16*cos(theta)**18 - 1.17021388769759e+16*cos(theta)**16 + 3.31192609725732e+15*cos(theta)**14 - 656612799238380.0*cos(theta)**12 + 88441723979047.1*cos(theta)**10 - 7698022396628.86*cos(theta)**8 + 399156716862.237*cos(theta)**6 - 10710824244.9616*cos(theta)**4 + 111959835.313188*cos(theta)**2 - 191384.333868697)*cos(4*phi)

#@torch.jit.script
def Yl34_m5(theta, phi):
    return 6.89940251833707e-8*(1.0 - cos(theta)**2)**2.5*(5.53012092742222e+16*cos(theta)**29 - 3.35108820378123e+17*cos(theta)**27 + 9.04793815020931e+17*cos(theta)**25 - 1.43618065876338e+18*cos(theta)**23 + 1.48915453552105e+18*cos(theta)**21 - 1.06007611003193e+18*cos(theta)**19 + 5.30038055015966e+17*cos(theta)**17 - 1.87234222031614e+17*cos(theta)**15 + 4.63669653616025e+16*cos(theta)**13 - 7.87935359086056e+15*cos(theta)**11 + 884417239790471.0*cos(theta)**9 - 61584179173030.9*cos(theta)**7 + 2394940301173.42*cos(theta)**5 - 42843296979.8466*cos(theta)**3 + 223919670.626376*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl34_m6(theta, phi):
    return 2.0257343306691e-9*(1.0 - cos(theta)**2)**3*(1.60373506895244e+18*cos(theta)**28 - 9.04793815020931e+18*cos(theta)**26 + 2.26198453755233e+19*cos(theta)**24 - 3.30321551515578e+19*cos(theta)**22 + 3.1272245245942e+19*cos(theta)**20 - 2.01414460906067e+19*cos(theta)**18 + 9.01064693527143e+18*cos(theta)**16 - 2.80851333047421e+18*cos(theta)**14 + 6.02770549700833e+17*cos(theta)**12 - 8.66728894994662e+16*cos(theta)**10 + 7.95975515811424e+15*cos(theta)**8 - 431089254211216.0*cos(theta)**6 + 11974701505867.1*cos(theta)**4 - 128529890939.54*cos(theta)**2 + 223919670.626376)*cos(6*phi)

#@torch.jit.script
def Yl34_m7(theta, phi):
    return 5.97876583646464e-11*(1.0 - cos(theta)**2)**3.5*(4.49045819306684e+19*cos(theta)**27 - 2.35246391905442e+20*cos(theta)**25 + 5.42876289012559e+20*cos(theta)**23 - 7.26707413334272e+20*cos(theta)**21 + 6.2544490491884e+20*cos(theta)**19 - 3.62546029630921e+20*cos(theta)**17 + 1.44170350964343e+20*cos(theta)**15 - 3.9319186626639e+19*cos(theta)**13 + 7.23324659641e+18*cos(theta)**11 - 8.66728894994662e+17*cos(theta)**9 + 6.36780412649139e+16*cos(theta)**7 - 2.5865355252673e+15*cos(theta)**5 + 47898806023468.5*cos(theta)**3 - 257059781879.079*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl34_m8(theta, phi):
    return 1.77543598061902e-12*(1.0 - cos(theta)**2)**4*(1.21242371212805e+21*cos(theta)**26 - 5.88115979763605e+21*cos(theta)**24 + 1.24861546472888e+22*cos(theta)**22 - 1.52608556800197e+22*cos(theta)**20 + 1.1883453193458e+22*cos(theta)**18 - 6.16328250372566e+21*cos(theta)**16 + 2.16255526446514e+21*cos(theta)**14 - 5.11149426146306e+20*cos(theta)**12 + 7.956571256051e+19*cos(theta)**10 - 7.80056005495196e+18*cos(theta)**8 + 4.45746288854398e+17*cos(theta)**6 - 1.29326776263365e+16*cos(theta)**4 + 143696418070405.0*cos(theta)**2 - 257059781879.079)*cos(8*phi)

#@torch.jit.script
def Yl34_m9(theta, phi):
    return 5.30987277141628e-14*(1.0 - cos(theta)**2)**4.5*(3.15230165153292e+22*cos(theta)**25 - 1.41147835143265e+23*cos(theta)**23 + 2.74695402240355e+23*cos(theta)**21 - 3.05217113600394e+23*cos(theta)**19 + 2.13902157482243e+23*cos(theta)**17 - 9.86125200596105e+22*cos(theta)**15 + 3.0275773702512e+22*cos(theta)**13 - 6.13379311375568e+21*cos(theta)**11 + 7.956571256051e+20*cos(theta)**9 - 6.24044804396157e+19*cos(theta)**7 + 2.67447773312639e+18*cos(theta)**5 - 5.17307105053459e+16*cos(theta)**3 + 287392836140811.0*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl34_m10(theta, phi):
    return 1.60098687884658e-15*(1.0 - cos(theta)**2)**5*(7.88075412883231e+23*cos(theta)**24 - 3.2464002082951e+24*cos(theta)**22 + 5.76860344704745e+24*cos(theta)**20 - 5.79912515840749e+24*cos(theta)**18 + 3.63633667719814e+24*cos(theta)**16 - 1.47918780089416e+24*cos(theta)**14 + 3.93585058132656e+23*cos(theta)**12 - 6.74717242513125e+22*cos(theta)**10 + 7.1609141304459e+21*cos(theta)**8 - 4.3683136307731e+20*cos(theta)**6 + 1.33723886656319e+19*cos(theta)**4 - 1.55192131516038e+17*cos(theta)**2 + 287392836140811.0)*cos(10*phi)

#@torch.jit.script
def Yl34_m11(theta, phi):
    return 4.87164793230034e-17*(1.0 - cos(theta)**2)**5.5*(1.89138099091975e+25*cos(theta)**23 - 7.14208045824922e+25*cos(theta)**21 + 1.15372068940949e+26*cos(theta)**19 - 1.04384252851335e+26*cos(theta)**17 + 5.81813868351702e+25*cos(theta)**15 - 2.07086292125182e+25*cos(theta)**13 + 4.72302069759187e+24*cos(theta)**11 - 6.74717242513125e+23*cos(theta)**9 + 5.72873130435672e+22*cos(theta)**7 - 2.62098817846386e+21*cos(theta)**5 + 5.34895546625277e+19*cos(theta)**3 - 3.10384263032076e+17*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl34_m12(theta, phi):
    return 1.49772838629695e-18*(1.0 - cos(theta)**2)**6*(4.35017627911543e+26*cos(theta)**22 - 1.49983689623234e+27*cos(theta)**20 + 2.19206930987803e+27*cos(theta)**18 - 1.77453229847269e+27*cos(theta)**16 + 8.72720802527553e+26*cos(theta)**14 - 2.69212179762737e+26*cos(theta)**12 + 5.19532276735106e+25*cos(theta)**10 - 6.07245518261812e+24*cos(theta)**8 + 4.0101119130497e+23*cos(theta)**6 - 1.31049408923193e+22*cos(theta)**4 + 1.60468663987583e+20*cos(theta)**2 - 3.10384263032076e+17)*cos(12*phi)

#@torch.jit.script
def Yl34_m13(theta, phi):
    return 4.65771371921163e-20*(1.0 - cos(theta)**2)**6.5*(9.57038781405396e+27*cos(theta)**21 - 2.99967379246467e+28*cos(theta)**19 + 3.94572475778045e+28*cos(theta)**17 - 2.83925167755631e+28*cos(theta)**15 + 1.22180912353857e+28*cos(theta)**13 - 3.23054615715284e+27*cos(theta)**11 + 5.19532276735106e+26*cos(theta)**9 - 4.8579641460945e+25*cos(theta)**7 + 2.40606714782982e+24*cos(theta)**5 - 5.24197635692772e+22*cos(theta)**3 + 3.20937327975166e+20*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl34_m14(theta, phi):
    return 1.46704192609139e-21*(1.0 - cos(theta)**2)**7*(2.00978144095133e+29*cos(theta)**20 - 5.69938020568288e+29*cos(theta)**18 + 6.70773208822677e+29*cos(theta)**16 - 4.25887751633446e+29*cos(theta)**14 + 1.58835186060015e+29*cos(theta)**12 - 3.55360077286812e+28*cos(theta)**10 + 4.67579049061595e+27*cos(theta)**8 - 3.40057490226615e+26*cos(theta)**6 + 1.20303357391491e+25*cos(theta)**4 - 1.57259290707831e+23*cos(theta)**2 + 3.20937327975166e+20)*cos(14*phi)

#@torch.jit.script
def Yl34_m15(theta, phi):
    return 4.68629353226083e-23*(1.0 - cos(theta)**2)**7.5*(4.01956288190266e+30*cos(theta)**19 - 1.02588843702292e+31*cos(theta)**17 + 1.07323713411628e+31*cos(theta)**15 - 5.96242852286824e+30*cos(theta)**13 + 1.90602223272018e+30*cos(theta)**11 - 3.55360077286812e+29*cos(theta)**9 + 3.74063239249276e+28*cos(theta)**7 - 2.04034494135969e+27*cos(theta)**5 + 4.81213429565964e+25*cos(theta)**3 - 3.14518581415663e+23*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl34_m16(theta, phi):
    return 1.52043439327851e-24*(1.0 - cos(theta)**2)**8*(7.63716947561506e+31*cos(theta)**18 - 1.74401034293896e+32*cos(theta)**16 + 1.60985570117443e+32*cos(theta)**14 - 7.75115707972871e+31*cos(theta)**12 + 2.09662445599219e+31*cos(theta)**10 - 3.19824069558131e+30*cos(theta)**8 + 2.61844267474493e+29*cos(theta)**6 - 1.02017247067984e+28*cos(theta)**4 + 1.44364028869789e+26*cos(theta)**2 - 3.14518581415663e+23)*cos(16*phi)

#@torch.jit.script
def Yl34_m17(theta, phi):
    return 5.01818126253981e-26*(1.0 - cos(theta)**2)**8.5*(1.37469050561071e+33*cos(theta)**17 - 2.79041654870234e+33*cos(theta)**15 + 2.2537979816442e+33*cos(theta)**13 - 9.30138849567446e+32*cos(theta)**11 + 2.09662445599219e+32*cos(theta)**9 - 2.55859255646505e+31*cos(theta)**7 + 1.57106560484696e+30*cos(theta)**5 - 4.08068988271938e+28*cos(theta)**3 + 2.88728057739579e+26*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl34_m18(theta, phi):
    return 1.6877970053263e-27*(1.0 - cos(theta)**2)**9*(2.33697385953821e+34*cos(theta)**16 - 4.18562482305351e+34*cos(theta)**14 + 2.92993737613745e+34*cos(theta)**12 - 1.02315273452419e+34*cos(theta)**10 + 1.88696201039297e+33*cos(theta)**8 - 1.79101478952553e+32*cos(theta)**6 + 7.8553280242348e+30*cos(theta)**4 - 1.22420696481581e+29*cos(theta)**2 + 2.88728057739579e+26)*cos(18*phi)

#@torch.jit.script
def Yl34_m19(theta, phi):
    return 5.79591871206322e-29*(1.0 - cos(theta)**2)**9.5*(3.73915817526113e+35*cos(theta)**15 - 5.85987475227491e+35*cos(theta)**13 + 3.51592485136495e+35*cos(theta)**11 - 1.02315273452419e+35*cos(theta)**9 + 1.50956960831438e+34*cos(theta)**7 - 1.07460887371532e+33*cos(theta)**5 + 3.14213120969392e+31*cos(theta)**3 - 2.44841392963163e+29*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl34_m20(theta, phi):
    return 2.03647825147882e-30*(1.0 - cos(theta)**2)**10*(5.6087372628917e+36*cos(theta)**14 - 7.61783717795738e+36*cos(theta)**12 + 3.86751733650144e+36*cos(theta)**10 - 9.20837461071771e+35*cos(theta)**8 + 1.05669872582007e+35*cos(theta)**6 - 5.3730443685766e+33*cos(theta)**4 + 9.42639362908176e+31*cos(theta)**2 - 2.44841392963163e+29)*cos(20*phi)

#@torch.jit.script
def Yl34_m21(theta, phi):
    return 7.33895819488808e-32*(1.0 - cos(theta)**2)**10.5*(7.85223216804838e+37*cos(theta)**13 - 9.14140461354886e+37*cos(theta)**11 + 3.86751733650144e+37*cos(theta)**9 - 7.36669968857417e+36*cos(theta)**7 + 6.34019235492039e+35*cos(theta)**5 - 2.14921774743064e+34*cos(theta)**3 + 1.88527872581635e+32*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl34_m22(theta, phi):
    return 2.71999887348259e-33*(1.0 - cos(theta)**2)**11*(1.02079018184629e+39*cos(theta)**12 - 1.00555450749037e+39*cos(theta)**10 + 3.4807656028513e+38*cos(theta)**8 - 5.15668978200192e+37*cos(theta)**6 + 3.1700961774602e+36*cos(theta)**4 - 6.44765324229192e+34*cos(theta)**2 + 1.88527872581635e+32)*cos(22*phi)

#@torch.jit.script
def Yl34_m23(theta, phi):
    return 1.04001756281185e-34*(1.0 - cos(theta)**2)**11.5*(1.22494821821555e+40*cos(theta)**11 - 1.00555450749037e+40*cos(theta)**9 + 2.78461248228104e+39*cos(theta)**7 - 3.09401386920115e+38*cos(theta)**5 + 1.26803847098408e+37*cos(theta)**3 - 1.28953064845838e+35*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl34_m24(theta, phi):
    return 4.11746896065541e-36*(1.0 - cos(theta)**2)**12*(1.3474430400371e+41*cos(theta)**10 - 9.04999056741337e+40*cos(theta)**8 + 1.94922873759673e+40*cos(theta)**6 - 1.54700693460058e+39*cos(theta)**4 + 3.80411541295224e+37*cos(theta)**2 - 1.28953064845838e+35)*cos(24*phi)

#@torch.jit.script
def Yl34_m25(theta, phi):
    return 1.69513514495286e-37*(1.0 - cos(theta)**2)**12.5*(1.3474430400371e+42*cos(theta)**9 - 7.23999245393069e+41*cos(theta)**7 + 1.16953724255804e+41*cos(theta)**5 - 6.1880277384023e+39*cos(theta)**3 + 7.60823082590447e+37*cos(theta))*cos(25*phi)

#@torch.jit.script
def Yl34_m26(theta, phi):
    return 7.29470020663704e-39*(1.0 - cos(theta)**2)**13*(1.21269873603339e+43*cos(theta)**8 - 5.06799471775149e+42*cos(theta)**6 + 5.84768621279018e+41*cos(theta)**4 - 1.85640832152069e+40*cos(theta)**2 + 7.60823082590447e+37)*cos(26*phi)

#@torch.jit.script
def Yl34_m27(theta, phi):
    return 3.30215562682199e-40*(1.0 - cos(theta)**2)**13.5*(9.70158988826713e+43*cos(theta)**7 - 3.04079683065089e+43*cos(theta)**5 + 2.33907448511607e+42*cos(theta)**3 - 3.71281664304138e+40*cos(theta))*cos(27*phi)

#@torch.jit.script
def Yl34_m28(theta, phi):
    return 1.58508542441973e-41*(1.0 - cos(theta)**2)**14*(6.79111292178699e+44*cos(theta)**6 - 1.52039841532545e+44*cos(theta)**4 + 7.01722345534821e+42*cos(theta)**2 - 3.71281664304138e+40)*cos(28*phi)

#@torch.jit.script
def Yl34_m29(theta, phi):
    return 8.15279969880161e-43*(1.0 - cos(theta)**2)**14.5*(4.0746677530722e+45*cos(theta)**5 - 6.08159366130178e+44*cos(theta)**3 + 1.40344469106964e+43*cos(theta))*cos(29*phi)

#@torch.jit.script
def Yl34_m30(theta, phi):
    return 4.55755358336505e-44*(1.0 - cos(theta)**2)**15*(2.0373338765361e+46*cos(theta)**4 - 1.82447809839054e+45*cos(theta)**2 + 1.40344469106964e+43)*cos(30*phi)

#@torch.jit.script
def Yl34_m31(theta, phi):
    return 2.8264747454439e-45*(1.0 - cos(theta)**2)**15.5*(8.14933550614439e+46*cos(theta)**3 - 3.64895619678107e+45*cos(theta))*cos(31*phi)

#@torch.jit.script
def Yl34_m32(theta, phi):
    return 2.0086881349656e-46*(1.0 - cos(theta)**2)**16*(2.44480065184332e+47*cos(theta)**2 - 3.64895619678107e+45)*cos(32*phi)

#@torch.jit.script
def Yl34_m33(theta, phi):
    return 8.48464280026292*(1.0 - cos(theta)**2)**16.5*cos(33*phi)*cos(theta)

#@torch.jit.script
def Yl34_m34(theta, phi):
    return 1.0289140723859*(1.0 - cos(theta)**2)**17*cos(34*phi)

#@torch.jit.script
def Yl35_m_minus_35(theta, phi):
    return 1.03623739663619*(1.0 - cos(theta)**2)**17.5*sin(35*phi)

#@torch.jit.script
def Yl35_m_minus_34(theta, phi):
    return 8.66978407765238*(1.0 - cos(theta)**2)**17*sin(34*phi)*cos(theta)

#@torch.jit.script
def Yl35_m_minus_33(theta, phi):
    return 3.01873705359384e-48*(1.0 - cos(theta)**2)**16.5*(1.68691244977189e+49*cos(theta)**2 - 2.44480065184332e+47)*sin(33*phi)

#@torch.jit.script
def Yl35_m_minus_32(theta, phi):
    return 4.31161892256615e-47*(1.0 - cos(theta)**2)**16*(5.62304149923963e+48*cos(theta)**3 - 2.44480065184332e+47*cos(theta))*sin(32*phi)

#@torch.jit.script
def Yl35_m_minus_31(theta, phi):
    return 7.05842437981691e-46*(1.0 - cos(theta)**2)**15.5*(1.40576037480991e+48*cos(theta)**4 - 1.22240032592166e+47*cos(theta)**2 + 9.12239049195268e+44)*sin(31*phi)

#@torch.jit.script
def Yl35_m_minus_30(theta, phi):
    return 1.28222646437538e-44*(1.0 - cos(theta)**2)**15*(2.81152074961981e+47*cos(theta)**5 - 4.0746677530722e+46*cos(theta)**3 + 9.12239049195268e+44*cos(theta))*sin(30*phi)

#@torch.jit.script
def Yl35_m_minus_29(theta, phi):
    return 2.53219437507943e-43*(1.0 - cos(theta)**2)**14.5*(4.68586791603302e+46*cos(theta)**6 - 1.01866693826805e+46*cos(theta)**4 + 4.56119524597634e+44*cos(theta)**2 - 2.33907448511607e+42)*sin(29*phi)

#@torch.jit.script
def Yl35_m_minus_28(theta, phi):
    return 5.35964527018943e-42*(1.0 - cos(theta)**2)**14*(6.69409702290432e+45*cos(theta)**7 - 2.0373338765361e+45*cos(theta)**5 + 1.52039841532545e+44*cos(theta)**3 - 2.33907448511607e+42*cos(theta))*sin(28*phi)

#@torch.jit.script
def Yl35_m_minus_27(theta, phi):
    return 1.20323737894154e-40*(1.0 - cos(theta)**2)**13.5*(8.3676212786304e+44*cos(theta)**8 - 3.3955564608935e+44*cos(theta)**6 + 3.80099603831361e+43*cos(theta)**4 - 1.16953724255804e+42*cos(theta)**2 + 4.64102080380173e+39)*sin(27*phi)

#@torch.jit.script
def Yl35_m_minus_26(theta, phi):
    return 2.8422901788273e-39*(1.0 - cos(theta)**2)**13*(9.297356976256e+43*cos(theta)**9 - 4.85079494413357e+43*cos(theta)**7 + 7.60199207662723e+42*cos(theta)**5 - 3.89845747519345e+41*cos(theta)**3 + 4.64102080380173e+39*cos(theta))*sin(26*phi)

#@torch.jit.script
def Yl35_m_minus_25(theta, phi):
    return 7.01993889645875e-38*(1.0 - cos(theta)**2)**12.5*(9.297356976256e+42*cos(theta)**10 - 6.06349368016696e+42*cos(theta)**8 + 1.26699867943787e+42*cos(theta)**6 - 9.74614368798363e+40*cos(theta)**4 + 2.32051040190086e+39*cos(theta)**2 - 7.60823082590447e+36)*sin(25*phi)

#@torch.jit.script
def Yl35_m_minus_24(theta, phi):
    return 1.80345495626061e-36*(1.0 - cos(theta)**2)**12*(8.45214270568727e+41*cos(theta)**11 - 6.73721520018551e+41*cos(theta)**9 + 1.80999811348267e+41*cos(theta)**7 - 1.94922873759673e+40*cos(theta)**5 + 7.73503467300288e+38*cos(theta)**3 - 7.60823082590447e+36*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl35_m_minus_23(theta, phi):
    return 4.79868153112577e-35*(1.0 - cos(theta)**2)**11.5*(7.04345225473939e+40*cos(theta)**12 - 6.73721520018551e+40*cos(theta)**10 + 2.26249764185334e+40*cos(theta)**8 - 3.24871456266121e+39*cos(theta)**6 + 1.93375866825072e+38*cos(theta)**4 - 3.80411541295224e+36*cos(theta)**2 + 1.07460887371532e+34)*sin(23*phi)

#@torch.jit.script
def Yl35_m_minus_22(theta, phi):
    return 1.31767286173862e-33*(1.0 - cos(theta)**2)**11*(5.41804019595338e+39*cos(theta)**13 - 6.12474109107773e+39*cos(theta)**11 + 2.51388626872594e+39*cos(theta)**9 - 4.64102080380173e+38*cos(theta)**7 + 3.86751733650144e+37*cos(theta)**5 - 1.26803847098408e+36*cos(theta)**3 + 1.07460887371532e+34*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl35_m_minus_21(theta, phi):
    return 3.72228007128537e-32*(1.0 - cos(theta)**2)**10.5*(3.87002871139527e+38*cos(theta)**14 - 5.10395090923145e+38*cos(theta)**12 + 2.51388626872594e+38*cos(theta)**10 - 5.80127600475216e+37*cos(theta)**8 + 6.4458622275024e+36*cos(theta)**6 - 3.1700961774602e+35*cos(theta)**4 + 5.3730443685766e+33*cos(theta)**2 - 1.34662766129739e+31)*sin(21*phi)

#@torch.jit.script
def Yl35_m_minus_20(theta, phi):
    return 1.07881925735658e-30*(1.0 - cos(theta)**2)**10*(2.58001914093018e+37*cos(theta)**15 - 3.92611608402419e+37*cos(theta)**13 + 2.28535115338721e+37*cos(theta)**11 - 6.4458622275024e+36*cos(theta)**9 + 9.20837461071771e+35*cos(theta)**7 - 6.34019235492039e+34*cos(theta)**5 + 1.79101478952553e+33*cos(theta)**3 - 1.34662766129739e+31*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl35_m_minus_19(theta, phi):
    return 3.20029509770303e-29*(1.0 - cos(theta)**2)**9.5*(1.61251196308136e+36*cos(theta)**16 - 2.80436863144585e+36*cos(theta)**14 + 1.90445929448935e+36*cos(theta)**12 - 6.4458622275024e+35*cos(theta)**10 + 1.15104682633971e+35*cos(theta)**8 - 1.05669872582007e+34*cos(theta)**6 + 4.47753697381384e+32*cos(theta)**4 - 6.73313830648697e+30*cos(theta)**2 + 1.53025870601977e+28)*sin(19*phi)

#@torch.jit.script
def Yl35_m_minus_18(theta, phi):
    return 9.6964188430403e-28*(1.0 - cos(theta)**2)**9*(9.4853644887139e+34*cos(theta)**17 - 1.86957908763057e+35*cos(theta)**15 + 1.46496868806873e+35*cos(theta)**13 - 5.85987475227491e+34*cos(theta)**11 + 1.27894091815524e+34*cos(theta)**9 - 1.50956960831438e+33*cos(theta)**7 + 8.95507394762767e+31*cos(theta)**5 - 2.24437943549566e+30*cos(theta)**3 + 1.53025870601977e+28*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl35_m_minus_17(theta, phi):
    return 2.9949222630012e-26*(1.0 - cos(theta)**2)**8.5*(5.26964693817439e+33*cos(theta)**18 - 1.1684869297691e+34*cos(theta)**16 + 1.04640620576338e+34*cos(theta)**14 - 4.88322896022909e+33*cos(theta)**12 + 1.27894091815524e+33*cos(theta)**10 - 1.88696201039297e+32*cos(theta)**8 + 1.49251232460461e+31*cos(theta)**6 - 5.61094858873914e+29*cos(theta)**4 + 7.65129353009883e+27*cos(theta)**2 - 1.60404476521988e+25)*sin(17*phi)

#@torch.jit.script
def Yl35_m_minus_16(theta, phi):
    return 9.41377960708832e-25*(1.0 - cos(theta)**2)**8*(2.77349838851284e+32*cos(theta)**19 - 6.87345252805355e+32*cos(theta)**17 + 6.97604137175584e+32*cos(theta)**15 - 3.75632996940699e+32*cos(theta)**13 + 1.16267356195931e+32*cos(theta)**11 - 2.09662445599219e+31*cos(theta)**9 + 2.13216046372087e+30*cos(theta)**7 - 1.12218971774783e+29*cos(theta)**5 + 2.55043117669961e+27*cos(theta)**3 - 1.60404476521988e+25*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl35_m_minus_15(theta, phi):
    return 3.00652010504917e-23*(1.0 - cos(theta)**2)**7.5*(1.38674919425642e+31*cos(theta)**20 - 3.81858473780753e+31*cos(theta)**18 + 4.3600258573474e+31*cos(theta)**16 - 2.68309283529071e+31*cos(theta)**14 + 9.68894634966089e+30*cos(theta)**12 - 2.09662445599219e+30*cos(theta)**10 + 2.66520057965109e+29*cos(theta)**8 - 1.87031619624638e+28*cos(theta)**6 + 6.37607794174903e+26*cos(theta)**4 - 8.02022382609941e+24*cos(theta)**2 + 1.57259290707831e+22)*sin(15*phi)

#@torch.jit.script
def Yl35_m_minus_14(theta, phi):
    return 9.74223860268681e-22*(1.0 - cos(theta)**2)**7*(6.60356759169723e+29*cos(theta)**21 - 2.00978144095133e+30*cos(theta)**19 + 2.5647210925573e+30*cos(theta)**17 - 1.78872855686047e+30*cos(theta)**15 + 7.4530356535853e+29*cos(theta)**13 - 1.90602223272018e+29*cos(theta)**11 + 2.9613339773901e+28*cos(theta)**9 - 2.67188028035197e+27*cos(theta)**7 + 1.27521558834981e+26*cos(theta)**5 - 2.67340794203313e+24*cos(theta)**3 + 1.57259290707831e+22*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl35_m_minus_13(theta, phi):
    return 3.19866046346017e-20*(1.0 - cos(theta)**2)**6.5*(3.00162163258965e+28*cos(theta)**22 - 1.00489072047567e+29*cos(theta)**20 + 1.42484505142072e+29*cos(theta)**18 - 1.1179553480378e+29*cos(theta)**16 + 5.32359689541807e+28*cos(theta)**14 - 1.58835186060015e+28*cos(theta)**12 + 2.9613339773901e+27*cos(theta)**10 - 3.33985035043997e+26*cos(theta)**8 + 2.12535931391634e+25*cos(theta)**6 - 6.68351985508284e+23*cos(theta)**4 + 7.86296453539157e+21*cos(theta)**2 - 1.45880603625076e+19)*sin(13*phi)

#@torch.jit.script
def Yl35_m_minus_12(theta, phi):
    return 1.06280277340603e-18*(1.0 - cos(theta)**2)**6*(1.30505288373463e+27*cos(theta)**23 - 4.78519390702698e+27*cos(theta)**21 + 7.49918448116168e+27*cos(theta)**19 - 6.57620792963409e+27*cos(theta)**17 + 3.54906459694538e+27*cos(theta)**15 - 1.22180912353857e+27*cos(theta)**13 + 2.69212179762737e+26*cos(theta)**11 - 3.71094483382218e+25*cos(theta)**9 + 3.03622759130906e+24*cos(theta)**7 - 1.33670397101657e+23*cos(theta)**5 + 2.62098817846386e+21*cos(theta)**3 - 1.45880603625076e+19*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl35_m_minus_11(theta, phi):
    return 3.56949870606501e-17*(1.0 - cos(theta)**2)**5.5*(5.43772034889429e+25*cos(theta)**24 - 2.17508813955772e+26*cos(theta)**22 + 3.74959224058084e+26*cos(theta)**20 - 3.65344884979672e+26*cos(theta)**18 + 2.21816537309086e+26*cos(theta)**16 - 8.72720802527553e+25*cos(theta)**14 + 2.24343483135614e+25*cos(theta)**12 - 3.71094483382219e+24*cos(theta)**10 + 3.79528448913633e+23*cos(theta)**8 - 2.22783995169428e+22*cos(theta)**6 + 6.55247044615964e+20*cos(theta)**4 - 7.29403018125378e+18*cos(theta)**2 + 1.29326776263365e+16)*sin(11*phi)

#@torch.jit.script
def Yl35_m_minus_10(theta, phi):
    return 1.21047590494358e-15*(1.0 - cos(theta)**2)**5*(2.17508813955772e+24*cos(theta)**25 - 9.45690495459877e+24*cos(theta)**23 + 1.78552011456231e+25*cos(theta)**21 - 1.92286781568248e+25*cos(theta)**19 + 1.30480316064168e+25*cos(theta)**17 - 5.81813868351702e+24*cos(theta)**15 + 1.72571910104318e+24*cos(theta)**13 - 3.37358621256562e+23*cos(theta)**11 + 4.21698276570703e+22*cos(theta)**9 - 3.1826285024204e+21*cos(theta)**7 + 1.31049408923193e+20*cos(theta)**5 - 2.43134339375126e+18*cos(theta)**3 + 1.29326776263365e+16*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl35_m_minus_9(theta, phi):
    return 4.14046463847392e-14*(1.0 - cos(theta)**2)**4.5*(8.36572361368353e+22*cos(theta)**26 - 3.94037706441615e+23*cos(theta)**24 + 8.11600052073775e+23*cos(theta)**22 - 9.61433907841241e+23*cos(theta)**20 + 7.24890644800936e+23*cos(theta)**18 - 3.63633667719814e+23*cos(theta)**16 + 1.23265650074513e+23*cos(theta)**14 - 2.81132184380469e+22*cos(theta)**12 + 4.21698276570703e+21*cos(theta)**10 - 3.9782856280255e+20*cos(theta)**8 + 2.18415681538655e+19*cos(theta)**6 - 6.07835848437815e+17*cos(theta)**4 + 6.46633881316824e+15*cos(theta)**2 - 11053570620800.4)*sin(9*phi)

#@torch.jit.script
def Yl35_m_minus_8(theta, phi):
    return 1.42710951008933e-12*(1.0 - cos(theta)**2)**4*(3.09841615321612e+21*cos(theta)**27 - 1.57615082576646e+22*cos(theta)**25 + 3.52869587858163e+22*cos(theta)**23 - 4.57825670400591e+22*cos(theta)**21 + 3.81521392000493e+22*cos(theta)**19 - 2.13902157482243e+22*cos(theta)**17 + 8.21771000496754e+21*cos(theta)**15 - 2.16255526446514e+21*cos(theta)**13 + 3.8336206960973e+20*cos(theta)**11 - 4.42031736447278e+19*cos(theta)**9 + 3.12022402198078e+18*cos(theta)**7 - 1.21567169687563e+17*cos(theta)**5 + 2.15544627105608e+15*cos(theta)**3 - 11053570620800.4*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl35_m_minus_7(theta, phi):
    return 4.95188492471306e-11*(1.0 - cos(theta)**2)**3.5*(1.10657719757719e+20*cos(theta)**28 - 6.06211856064024e+20*cos(theta)**26 + 1.47028994940901e+21*cos(theta)**24 - 2.08102577454814e+21*cos(theta)**22 + 1.90760696000246e+21*cos(theta)**20 - 1.1883453193458e+21*cos(theta)**18 + 5.13606875310471e+20*cos(theta)**16 - 1.54468233176082e+20*cos(theta)**14 + 3.19468391341442e+19*cos(theta)**12 - 4.42031736447278e+18*cos(theta)**10 + 3.90028002747598e+17*cos(theta)**8 - 2.02611949479272e+16*cos(theta)**6 + 538861567764020.0*cos(theta)**4 - 5526785310400.21*cos(theta)**2 + 9180706495.68141)*sin(7*phi)

#@torch.jit.script
def Yl35_m_minus_6(theta, phi):
    return 1.72820074431929e-9*(1.0 - cos(theta)**2)**3*(3.81578343992133e+18*cos(theta)**29 - 2.24522909653342e+19*cos(theta)**27 + 5.88115979763605e+19*cos(theta)**25 - 9.04793815020931e+19*cos(theta)**23 + 9.08384266667839e+19*cos(theta)**21 - 6.2544490491884e+19*cos(theta)**19 + 3.02121691359101e+19*cos(theta)**17 - 1.02978822117388e+19*cos(theta)**15 + 2.45744916416494e+18*cos(theta)**13 - 4.01847033133889e+17*cos(theta)**11 + 4.33364447497331e+16*cos(theta)**9 - 2.89445642113245e+15*cos(theta)**7 + 107772313552804.0*cos(theta)**5 - 1842261770133.4*cos(theta)**3 + 9180706495.68141*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl35_m_minus_5(theta, phi):
    return 6.06103432557419e-8*(1.0 - cos(theta)**2)**2.5*(1.27192781330711e+17*cos(theta)**30 - 8.01867534476222e+17*cos(theta)**28 + 2.26198453755233e+18*cos(theta)**26 - 3.76997422925388e+18*cos(theta)**24 + 4.12901939394472e+18*cos(theta)**22 - 3.1272245245942e+18*cos(theta)**20 + 1.67845384088389e+18*cos(theta)**18 - 6.43617638233673e+17*cos(theta)**16 + 1.75532083154638e+17*cos(theta)**14 - 3.34872527611574e+16*cos(theta)**12 + 4.33364447497331e+15*cos(theta)**10 - 361807052641557.0*cos(theta)**8 + 17962052258800.7*cos(theta)**6 - 460565442533.351*cos(theta)**4 + 4590353247.8407*cos(theta)**2 - 7463989.02087919)*sin(5*phi)

#@torch.jit.script
def Yl35_m_minus_4(theta, phi):
    return 2.13431042725227e-6*(1.0 - cos(theta)**2)**2*(4.10299294615197e+15*cos(theta)**31 - 2.76506046371111e+16*cos(theta)**29 + 8.37772050945307e+16*cos(theta)**27 - 1.50798969170155e+17*cos(theta)**25 + 1.79522582345423e+17*cos(theta)**23 - 1.48915453552105e+17*cos(theta)**21 + 8.83396758359944e+16*cos(theta)**19 - 3.7859861072569e+16*cos(theta)**17 + 1.17021388769759e+16*cos(theta)**15 - 2.57594252008903e+15*cos(theta)**13 + 393967679543028.0*cos(theta)**11 - 40200783626839.6*cos(theta)**9 + 2566007465542.95*cos(theta)**7 - 92113088506.6701*cos(theta)**5 + 1530117749.28023*cos(theta)**3 - 7463989.02087919*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl35_m_minus_3(theta, phi):
    return 7.53988772320084e-5*(1.0 - cos(theta)**2)**1.5*(128218529567249.0*cos(theta)**32 - 921686821237037.0*cos(theta)**30 + 2.99204303909038e+15*cos(theta)**28 - 5.79996035269828e+15*cos(theta)**26 + 7.48010759772595e+15*cos(theta)**24 - 6.7688842523684e+15*cos(theta)**22 + 4.41698379179972e+15*cos(theta)**20 - 2.10332561514272e+15*cos(theta)**18 + 731383679810993.0*cos(theta)**16 - 183995894292074.0*cos(theta)**14 + 32830639961919.0*cos(theta)**12 - 4020078362683.96*cos(theta)**10 + 320750933192.869*cos(theta)**8 - 15352181417.7784*cos(theta)**6 + 382529437.320059*cos(theta)**4 - 3731994.5104396*cos(theta)**2 + 5980.76043339679)*sin(3*phi)

#@torch.jit.script
def Yl35_m_minus_2(theta, phi):
    return 0.00267001466710592*(1.0 - cos(theta)**2)*(3885409986886.33*cos(theta)**33 - 29731832943130.2*cos(theta)**31 + 103173897899668.0*cos(theta)**29 - 214813346396232.0*cos(theta)**27 + 299204303909038.0*cos(theta)**25 - 294299315320365.0*cos(theta)**23 + 210332561514272.0*cos(theta)**21 - 110701348165407.0*cos(theta)**19 + 43022569400646.6*cos(theta)**17 - 12266392952804.9*cos(theta)**15 + 2525433843224.54*cos(theta)**13 - 365461669334.906*cos(theta)**11 + 35638992576.9855*cos(theta)**9 - 2193168773.96834*cos(theta)**7 + 76505887.4640117*cos(theta)**5 - 1243998.17014653*cos(theta)**3 + 5980.76043339679*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl35_m_minus_1(theta, phi):
    return 0.09470086974142*(1.0 - cos(theta)**2)**0.5*(114276764320.186*cos(theta)**34 - 929119779472.819*cos(theta)**32 + 3439129929988.94*cos(theta)**30 - 7671905228436.87*cos(theta)**28 + 11507857842655.3*cos(theta)**26 - 12262471471681.9*cos(theta)**24 + 9560570977921.47*cos(theta)**22 - 5535067408270.33*cos(theta)**20 + 2390142744480.37*cos(theta)**18 - 766649559550.307*cos(theta)**16 + 180388131658.896*cos(theta)**14 - 30455139111.2421*cos(theta)**12 + 3563899257.69855*cos(theta)**10 - 274146096.746042*cos(theta)**8 + 12750981.244002*cos(theta)**6 - 310999.542536633*cos(theta)**4 + 2990.3802166984*cos(theta)**2 - 4.75418158457614)*sin(phi)

#@torch.jit.script
def Yl35_m0(theta, phi):
    return 24381701263.8311*cos(theta)**35 - 210248003651.877*cos(theta)**33 + 828439894986.499*cos(theta)**31 - 1975510518813.96*cos(theta)**29 + 3182766946978.05*cos(theta)**27 - 3662790814391.13*cos(theta)**25 + 3104060012195.87*cos(theta)**23 - 1968238554099.14*cos(theta)**21 + 939386582638.224*cos(theta)**19 - 336761227738.231*cos(theta)**17 + 89802994063.5284*cos(theta)**15 - 17494089752.6354*cos(theta)**13 + 2419395391.32192*cos(theta)**11 - 227464523.970437*cos(theta)**9 + 13602529.6726507*cos(theta)**7 - 464476.62296856*cos(theta)**5 + 7443.53562449616*cos(theta)**3 - 35.5017597352758*cos(theta)

#@torch.jit.script
def Yl35_m1(theta, phi):
    return 0.09470086974142*(1.0 - cos(theta)**2)**0.5*(114276764320.186*cos(theta)**34 - 929119779472.819*cos(theta)**32 + 3439129929988.94*cos(theta)**30 - 7671905228436.87*cos(theta)**28 + 11507857842655.3*cos(theta)**26 - 12262471471681.9*cos(theta)**24 + 9560570977921.47*cos(theta)**22 - 5535067408270.33*cos(theta)**20 + 2390142744480.37*cos(theta)**18 - 766649559550.307*cos(theta)**16 + 180388131658.896*cos(theta)**14 - 30455139111.2421*cos(theta)**12 + 3563899257.69855*cos(theta)**10 - 274146096.746042*cos(theta)**8 + 12750981.244002*cos(theta)**6 - 310999.542536633*cos(theta)**4 + 2990.3802166984*cos(theta)**2 - 4.75418158457614)*cos(phi)

#@torch.jit.script
def Yl35_m2(theta, phi):
    return 0.00267001466710592*(1.0 - cos(theta)**2)*(3885409986886.33*cos(theta)**33 - 29731832943130.2*cos(theta)**31 + 103173897899668.0*cos(theta)**29 - 214813346396232.0*cos(theta)**27 + 299204303909038.0*cos(theta)**25 - 294299315320365.0*cos(theta)**23 + 210332561514272.0*cos(theta)**21 - 110701348165407.0*cos(theta)**19 + 43022569400646.6*cos(theta)**17 - 12266392952804.9*cos(theta)**15 + 2525433843224.54*cos(theta)**13 - 365461669334.906*cos(theta)**11 + 35638992576.9855*cos(theta)**9 - 2193168773.96834*cos(theta)**7 + 76505887.4640117*cos(theta)**5 - 1243998.17014653*cos(theta)**3 + 5980.76043339679*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl35_m3(theta, phi):
    return 7.53988772320084e-5*(1.0 - cos(theta)**2)**1.5*(128218529567249.0*cos(theta)**32 - 921686821237037.0*cos(theta)**30 + 2.99204303909038e+15*cos(theta)**28 - 5.79996035269828e+15*cos(theta)**26 + 7.48010759772595e+15*cos(theta)**24 - 6.7688842523684e+15*cos(theta)**22 + 4.41698379179972e+15*cos(theta)**20 - 2.10332561514272e+15*cos(theta)**18 + 731383679810993.0*cos(theta)**16 - 183995894292074.0*cos(theta)**14 + 32830639961919.0*cos(theta)**12 - 4020078362683.96*cos(theta)**10 + 320750933192.869*cos(theta)**8 - 15352181417.7784*cos(theta)**6 + 382529437.320059*cos(theta)**4 - 3731994.5104396*cos(theta)**2 + 5980.76043339679)*cos(3*phi)

#@torch.jit.script
def Yl35_m4(theta, phi):
    return 2.13431042725227e-6*(1.0 - cos(theta)**2)**2*(4.10299294615197e+15*cos(theta)**31 - 2.76506046371111e+16*cos(theta)**29 + 8.37772050945307e+16*cos(theta)**27 - 1.50798969170155e+17*cos(theta)**25 + 1.79522582345423e+17*cos(theta)**23 - 1.48915453552105e+17*cos(theta)**21 + 8.83396758359944e+16*cos(theta)**19 - 3.7859861072569e+16*cos(theta)**17 + 1.17021388769759e+16*cos(theta)**15 - 2.57594252008903e+15*cos(theta)**13 + 393967679543028.0*cos(theta)**11 - 40200783626839.6*cos(theta)**9 + 2566007465542.95*cos(theta)**7 - 92113088506.6701*cos(theta)**5 + 1530117749.28023*cos(theta)**3 - 7463989.02087919*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl35_m5(theta, phi):
    return 6.06103432557419e-8*(1.0 - cos(theta)**2)**2.5*(1.27192781330711e+17*cos(theta)**30 - 8.01867534476222e+17*cos(theta)**28 + 2.26198453755233e+18*cos(theta)**26 - 3.76997422925388e+18*cos(theta)**24 + 4.12901939394472e+18*cos(theta)**22 - 3.1272245245942e+18*cos(theta)**20 + 1.67845384088389e+18*cos(theta)**18 - 6.43617638233673e+17*cos(theta)**16 + 1.75532083154638e+17*cos(theta)**14 - 3.34872527611574e+16*cos(theta)**12 + 4.33364447497331e+15*cos(theta)**10 - 361807052641557.0*cos(theta)**8 + 17962052258800.7*cos(theta)**6 - 460565442533.351*cos(theta)**4 + 4590353247.8407*cos(theta)**2 - 7463989.02087919)*cos(5*phi)

#@torch.jit.script
def Yl35_m6(theta, phi):
    return 1.72820074431929e-9*(1.0 - cos(theta)**2)**3*(3.81578343992133e+18*cos(theta)**29 - 2.24522909653342e+19*cos(theta)**27 + 5.88115979763605e+19*cos(theta)**25 - 9.04793815020931e+19*cos(theta)**23 + 9.08384266667839e+19*cos(theta)**21 - 6.2544490491884e+19*cos(theta)**19 + 3.02121691359101e+19*cos(theta)**17 - 1.02978822117388e+19*cos(theta)**15 + 2.45744916416494e+18*cos(theta)**13 - 4.01847033133889e+17*cos(theta)**11 + 4.33364447497331e+16*cos(theta)**9 - 2.89445642113245e+15*cos(theta)**7 + 107772313552804.0*cos(theta)**5 - 1842261770133.4*cos(theta)**3 + 9180706495.68141*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl35_m7(theta, phi):
    return 4.95188492471306e-11*(1.0 - cos(theta)**2)**3.5*(1.10657719757719e+20*cos(theta)**28 - 6.06211856064024e+20*cos(theta)**26 + 1.47028994940901e+21*cos(theta)**24 - 2.08102577454814e+21*cos(theta)**22 + 1.90760696000246e+21*cos(theta)**20 - 1.1883453193458e+21*cos(theta)**18 + 5.13606875310471e+20*cos(theta)**16 - 1.54468233176082e+20*cos(theta)**14 + 3.19468391341442e+19*cos(theta)**12 - 4.42031736447278e+18*cos(theta)**10 + 3.90028002747598e+17*cos(theta)**8 - 2.02611949479272e+16*cos(theta)**6 + 538861567764020.0*cos(theta)**4 - 5526785310400.21*cos(theta)**2 + 9180706495.68141)*cos(7*phi)

#@torch.jit.script
def Yl35_m8(theta, phi):
    return 1.42710951008933e-12*(1.0 - cos(theta)**2)**4*(3.09841615321612e+21*cos(theta)**27 - 1.57615082576646e+22*cos(theta)**25 + 3.52869587858163e+22*cos(theta)**23 - 4.57825670400591e+22*cos(theta)**21 + 3.81521392000493e+22*cos(theta)**19 - 2.13902157482243e+22*cos(theta)**17 + 8.21771000496754e+21*cos(theta)**15 - 2.16255526446514e+21*cos(theta)**13 + 3.8336206960973e+20*cos(theta)**11 - 4.42031736447278e+19*cos(theta)**9 + 3.12022402198078e+18*cos(theta)**7 - 1.21567169687563e+17*cos(theta)**5 + 2.15544627105608e+15*cos(theta)**3 - 11053570620800.4*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl35_m9(theta, phi):
    return 4.14046463847392e-14*(1.0 - cos(theta)**2)**4.5*(8.36572361368353e+22*cos(theta)**26 - 3.94037706441615e+23*cos(theta)**24 + 8.11600052073775e+23*cos(theta)**22 - 9.61433907841241e+23*cos(theta)**20 + 7.24890644800936e+23*cos(theta)**18 - 3.63633667719814e+23*cos(theta)**16 + 1.23265650074513e+23*cos(theta)**14 - 2.81132184380469e+22*cos(theta)**12 + 4.21698276570703e+21*cos(theta)**10 - 3.9782856280255e+20*cos(theta)**8 + 2.18415681538655e+19*cos(theta)**6 - 6.07835848437815e+17*cos(theta)**4 + 6.46633881316824e+15*cos(theta)**2 - 11053570620800.4)*cos(9*phi)

#@torch.jit.script
def Yl35_m10(theta, phi):
    return 1.21047590494358e-15*(1.0 - cos(theta)**2)**5*(2.17508813955772e+24*cos(theta)**25 - 9.45690495459877e+24*cos(theta)**23 + 1.78552011456231e+25*cos(theta)**21 - 1.92286781568248e+25*cos(theta)**19 + 1.30480316064168e+25*cos(theta)**17 - 5.81813868351702e+24*cos(theta)**15 + 1.72571910104318e+24*cos(theta)**13 - 3.37358621256562e+23*cos(theta)**11 + 4.21698276570703e+22*cos(theta)**9 - 3.1826285024204e+21*cos(theta)**7 + 1.31049408923193e+20*cos(theta)**5 - 2.43134339375126e+18*cos(theta)**3 + 1.29326776263365e+16*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl35_m11(theta, phi):
    return 3.56949870606501e-17*(1.0 - cos(theta)**2)**5.5*(5.43772034889429e+25*cos(theta)**24 - 2.17508813955772e+26*cos(theta)**22 + 3.74959224058084e+26*cos(theta)**20 - 3.65344884979672e+26*cos(theta)**18 + 2.21816537309086e+26*cos(theta)**16 - 8.72720802527553e+25*cos(theta)**14 + 2.24343483135614e+25*cos(theta)**12 - 3.71094483382219e+24*cos(theta)**10 + 3.79528448913633e+23*cos(theta)**8 - 2.22783995169428e+22*cos(theta)**6 + 6.55247044615964e+20*cos(theta)**4 - 7.29403018125378e+18*cos(theta)**2 + 1.29326776263365e+16)*cos(11*phi)

#@torch.jit.script
def Yl35_m12(theta, phi):
    return 1.06280277340603e-18*(1.0 - cos(theta)**2)**6*(1.30505288373463e+27*cos(theta)**23 - 4.78519390702698e+27*cos(theta)**21 + 7.49918448116168e+27*cos(theta)**19 - 6.57620792963409e+27*cos(theta)**17 + 3.54906459694538e+27*cos(theta)**15 - 1.22180912353857e+27*cos(theta)**13 + 2.69212179762737e+26*cos(theta)**11 - 3.71094483382218e+25*cos(theta)**9 + 3.03622759130906e+24*cos(theta)**7 - 1.33670397101657e+23*cos(theta)**5 + 2.62098817846386e+21*cos(theta)**3 - 1.45880603625076e+19*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl35_m13(theta, phi):
    return 3.19866046346017e-20*(1.0 - cos(theta)**2)**6.5*(3.00162163258965e+28*cos(theta)**22 - 1.00489072047567e+29*cos(theta)**20 + 1.42484505142072e+29*cos(theta)**18 - 1.1179553480378e+29*cos(theta)**16 + 5.32359689541807e+28*cos(theta)**14 - 1.58835186060015e+28*cos(theta)**12 + 2.9613339773901e+27*cos(theta)**10 - 3.33985035043997e+26*cos(theta)**8 + 2.12535931391634e+25*cos(theta)**6 - 6.68351985508284e+23*cos(theta)**4 + 7.86296453539157e+21*cos(theta)**2 - 1.45880603625076e+19)*cos(13*phi)

#@torch.jit.script
def Yl35_m14(theta, phi):
    return 9.74223860268681e-22*(1.0 - cos(theta)**2)**7*(6.60356759169723e+29*cos(theta)**21 - 2.00978144095133e+30*cos(theta)**19 + 2.5647210925573e+30*cos(theta)**17 - 1.78872855686047e+30*cos(theta)**15 + 7.4530356535853e+29*cos(theta)**13 - 1.90602223272018e+29*cos(theta)**11 + 2.9613339773901e+28*cos(theta)**9 - 2.67188028035197e+27*cos(theta)**7 + 1.27521558834981e+26*cos(theta)**5 - 2.67340794203313e+24*cos(theta)**3 + 1.57259290707831e+22*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl35_m15(theta, phi):
    return 3.00652010504917e-23*(1.0 - cos(theta)**2)**7.5*(1.38674919425642e+31*cos(theta)**20 - 3.81858473780753e+31*cos(theta)**18 + 4.3600258573474e+31*cos(theta)**16 - 2.68309283529071e+31*cos(theta)**14 + 9.68894634966089e+30*cos(theta)**12 - 2.09662445599219e+30*cos(theta)**10 + 2.66520057965109e+29*cos(theta)**8 - 1.87031619624638e+28*cos(theta)**6 + 6.37607794174903e+26*cos(theta)**4 - 8.02022382609941e+24*cos(theta)**2 + 1.57259290707831e+22)*cos(15*phi)

#@torch.jit.script
def Yl35_m16(theta, phi):
    return 9.41377960708832e-25*(1.0 - cos(theta)**2)**8*(2.77349838851284e+32*cos(theta)**19 - 6.87345252805355e+32*cos(theta)**17 + 6.97604137175584e+32*cos(theta)**15 - 3.75632996940699e+32*cos(theta)**13 + 1.16267356195931e+32*cos(theta)**11 - 2.09662445599219e+31*cos(theta)**9 + 2.13216046372087e+30*cos(theta)**7 - 1.12218971774783e+29*cos(theta)**5 + 2.55043117669961e+27*cos(theta)**3 - 1.60404476521988e+25*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl35_m17(theta, phi):
    return 2.9949222630012e-26*(1.0 - cos(theta)**2)**8.5*(5.26964693817439e+33*cos(theta)**18 - 1.1684869297691e+34*cos(theta)**16 + 1.04640620576338e+34*cos(theta)**14 - 4.88322896022909e+33*cos(theta)**12 + 1.27894091815524e+33*cos(theta)**10 - 1.88696201039297e+32*cos(theta)**8 + 1.49251232460461e+31*cos(theta)**6 - 5.61094858873914e+29*cos(theta)**4 + 7.65129353009883e+27*cos(theta)**2 - 1.60404476521988e+25)*cos(17*phi)

#@torch.jit.script
def Yl35_m18(theta, phi):
    return 9.6964188430403e-28*(1.0 - cos(theta)**2)**9*(9.4853644887139e+34*cos(theta)**17 - 1.86957908763057e+35*cos(theta)**15 + 1.46496868806873e+35*cos(theta)**13 - 5.85987475227491e+34*cos(theta)**11 + 1.27894091815524e+34*cos(theta)**9 - 1.50956960831438e+33*cos(theta)**7 + 8.95507394762767e+31*cos(theta)**5 - 2.24437943549566e+30*cos(theta)**3 + 1.53025870601977e+28*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl35_m19(theta, phi):
    return 3.20029509770303e-29*(1.0 - cos(theta)**2)**9.5*(1.61251196308136e+36*cos(theta)**16 - 2.80436863144585e+36*cos(theta)**14 + 1.90445929448935e+36*cos(theta)**12 - 6.4458622275024e+35*cos(theta)**10 + 1.15104682633971e+35*cos(theta)**8 - 1.05669872582007e+34*cos(theta)**6 + 4.47753697381384e+32*cos(theta)**4 - 6.73313830648697e+30*cos(theta)**2 + 1.53025870601977e+28)*cos(19*phi)

#@torch.jit.script
def Yl35_m20(theta, phi):
    return 1.07881925735658e-30*(1.0 - cos(theta)**2)**10*(2.58001914093018e+37*cos(theta)**15 - 3.92611608402419e+37*cos(theta)**13 + 2.28535115338721e+37*cos(theta)**11 - 6.4458622275024e+36*cos(theta)**9 + 9.20837461071771e+35*cos(theta)**7 - 6.34019235492039e+34*cos(theta)**5 + 1.79101478952553e+33*cos(theta)**3 - 1.34662766129739e+31*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl35_m21(theta, phi):
    return 3.72228007128537e-32*(1.0 - cos(theta)**2)**10.5*(3.87002871139527e+38*cos(theta)**14 - 5.10395090923145e+38*cos(theta)**12 + 2.51388626872594e+38*cos(theta)**10 - 5.80127600475216e+37*cos(theta)**8 + 6.4458622275024e+36*cos(theta)**6 - 3.1700961774602e+35*cos(theta)**4 + 5.3730443685766e+33*cos(theta)**2 - 1.34662766129739e+31)*cos(21*phi)

#@torch.jit.script
def Yl35_m22(theta, phi):
    return 1.31767286173862e-33*(1.0 - cos(theta)**2)**11*(5.41804019595338e+39*cos(theta)**13 - 6.12474109107773e+39*cos(theta)**11 + 2.51388626872594e+39*cos(theta)**9 - 4.64102080380173e+38*cos(theta)**7 + 3.86751733650144e+37*cos(theta)**5 - 1.26803847098408e+36*cos(theta)**3 + 1.07460887371532e+34*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl35_m23(theta, phi):
    return 4.79868153112577e-35*(1.0 - cos(theta)**2)**11.5*(7.04345225473939e+40*cos(theta)**12 - 6.73721520018551e+40*cos(theta)**10 + 2.26249764185334e+40*cos(theta)**8 - 3.24871456266121e+39*cos(theta)**6 + 1.93375866825072e+38*cos(theta)**4 - 3.80411541295224e+36*cos(theta)**2 + 1.07460887371532e+34)*cos(23*phi)

#@torch.jit.script
def Yl35_m24(theta, phi):
    return 1.80345495626061e-36*(1.0 - cos(theta)**2)**12*(8.45214270568727e+41*cos(theta)**11 - 6.73721520018551e+41*cos(theta)**9 + 1.80999811348267e+41*cos(theta)**7 - 1.94922873759673e+40*cos(theta)**5 + 7.73503467300288e+38*cos(theta)**3 - 7.60823082590447e+36*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl35_m25(theta, phi):
    return 7.01993889645875e-38*(1.0 - cos(theta)**2)**12.5*(9.297356976256e+42*cos(theta)**10 - 6.06349368016696e+42*cos(theta)**8 + 1.26699867943787e+42*cos(theta)**6 - 9.74614368798363e+40*cos(theta)**4 + 2.32051040190086e+39*cos(theta)**2 - 7.60823082590447e+36)*cos(25*phi)

#@torch.jit.script
def Yl35_m26(theta, phi):
    return 2.8422901788273e-39*(1.0 - cos(theta)**2)**13*(9.297356976256e+43*cos(theta)**9 - 4.85079494413357e+43*cos(theta)**7 + 7.60199207662723e+42*cos(theta)**5 - 3.89845747519345e+41*cos(theta)**3 + 4.64102080380173e+39*cos(theta))*cos(26*phi)

#@torch.jit.script
def Yl35_m27(theta, phi):
    return 1.20323737894154e-40*(1.0 - cos(theta)**2)**13.5*(8.3676212786304e+44*cos(theta)**8 - 3.3955564608935e+44*cos(theta)**6 + 3.80099603831361e+43*cos(theta)**4 - 1.16953724255804e+42*cos(theta)**2 + 4.64102080380173e+39)*cos(27*phi)

#@torch.jit.script
def Yl35_m28(theta, phi):
    return 5.35964527018943e-42*(1.0 - cos(theta)**2)**14*(6.69409702290432e+45*cos(theta)**7 - 2.0373338765361e+45*cos(theta)**5 + 1.52039841532545e+44*cos(theta)**3 - 2.33907448511607e+42*cos(theta))*cos(28*phi)

#@torch.jit.script
def Yl35_m29(theta, phi):
    return 2.53219437507943e-43*(1.0 - cos(theta)**2)**14.5*(4.68586791603302e+46*cos(theta)**6 - 1.01866693826805e+46*cos(theta)**4 + 4.56119524597634e+44*cos(theta)**2 - 2.33907448511607e+42)*cos(29*phi)

#@torch.jit.script
def Yl35_m30(theta, phi):
    return 1.28222646437538e-44*(1.0 - cos(theta)**2)**15*(2.81152074961981e+47*cos(theta)**5 - 4.0746677530722e+46*cos(theta)**3 + 9.12239049195268e+44*cos(theta))*cos(30*phi)

#@torch.jit.script
def Yl35_m31(theta, phi):
    return 7.05842437981691e-46*(1.0 - cos(theta)**2)**15.5*(1.40576037480991e+48*cos(theta)**4 - 1.22240032592166e+47*cos(theta)**2 + 9.12239049195268e+44)*cos(31*phi)

#@torch.jit.script
def Yl35_m32(theta, phi):
    return 4.31161892256615e-47*(1.0 - cos(theta)**2)**16*(5.62304149923963e+48*cos(theta)**3 - 2.44480065184332e+47*cos(theta))*cos(32*phi)

#@torch.jit.script
def Yl35_m33(theta, phi):
    return 3.01873705359384e-48*(1.0 - cos(theta)**2)**16.5*(1.68691244977189e+49*cos(theta)**2 - 2.44480065184332e+47)*cos(33*phi)

#@torch.jit.script
def Yl35_m34(theta, phi):
    return 8.66978407765238*(1.0 - cos(theta)**2)**17*cos(34*phi)*cos(theta)

#@torch.jit.script
def Yl35_m35(theta, phi):
    return 1.03623739663619*(1.0 - cos(theta)**2)**17.5*cos(35*phi)

#@torch.jit.script
def Yl36_m_minus_36(theta, phi):
    return 1.04340867525942*(1.0 - cos(theta)**2)**18*sin(36*phi)

#@torch.jit.script
def Yl36_m_minus_35(theta, phi):
    return 8.85361619789771*(1.0 - cos(theta)**2)**17.5*sin(35*phi)*cos(theta)

#@torch.jit.script
def Yl36_m_minus_34(theta, phi):
    return 4.40437182605064e-50*(1.0 - cos(theta)**2)**17*(1.19770783933804e+51*cos(theta)**2 - 1.68691244977189e+49)*sin(34*phi)

#@torch.jit.script
def Yl36_m_minus_33(theta, phi):
    return 6.38254114616021e-49*(1.0 - cos(theta)**2)**16.5*(3.99235946446014e+50*cos(theta)**3 - 1.68691244977189e+49*cos(theta))*sin(33*phi)

#@torch.jit.script
def Yl36_m_minus_32(theta, phi):
    return 1.06034737181502e-47*(1.0 - cos(theta)**2)**16*(9.98089866115034e+49*cos(theta)**4 - 8.43456224885944e+48*cos(theta)**2 + 6.11200162960829e+46)*sin(32*phi)

#@torch.jit.script
def Yl36_m_minus_31(theta, phi):
    return 1.95518394692445e-46*(1.0 - cos(theta)**2)**15.5*(1.99617973223007e+49*cos(theta)**5 - 2.81152074961981e+48*cos(theta)**3 + 6.11200162960829e+46*cos(theta))*sin(31*phi)

#@torch.jit.script
def Yl36_m_minus_30(theta, phi):
    return 3.92013162413846e-45*(1.0 - cos(theta)**2)**15*(3.32696622038345e+48*cos(theta)**6 - 7.02880187404954e+47*cos(theta)**4 + 3.05600081480415e+46*cos(theta)**2 - 1.52039841532545e+44)*sin(30*phi)

#@torch.jit.script
def Yl36_m_minus_29(theta, phi):
    return 8.42600353736191e-44*(1.0 - cos(theta)**2)**14.5*(4.75280888626207e+47*cos(theta)**7 - 1.40576037480991e+47*cos(theta)**5 + 1.01866693826805e+46*cos(theta)**3 - 1.52039841532545e+44*cos(theta))*sin(29*phi)

#@torch.jit.script
def Yl36_m_minus_28(theta, phi):
    return 1.92142443301969e-42*(1.0 - cos(theta)**2)**14*(5.94101110782758e+46*cos(theta)**8 - 2.34293395801651e+46*cos(theta)**6 + 2.54666734567012e+45*cos(theta)**4 - 7.60199207662723e+43*cos(theta)**2 + 2.92384310639509e+41)*sin(28*phi)

#@torch.jit.script
def Yl36_m_minus_27(theta, phi):
    return 4.61141863924726e-41*(1.0 - cos(theta)**2)**13.5*(6.60112345314176e+45*cos(theta)**9 - 3.34704851145216e+45*cos(theta)**7 + 5.09333469134024e+44*cos(theta)**5 - 2.53399735887574e+43*cos(theta)**3 + 2.92384310639509e+41*cos(theta))*sin(27*phi)

#@torch.jit.script
def Yl36_m_minus_26(theta, phi):
    return 1.1574568923217e-39*(1.0 - cos(theta)**2)**13*(6.60112345314176e+44*cos(theta)**10 - 4.1838106393152e+44*cos(theta)**8 + 8.48889115223374e+43*cos(theta)**6 - 6.33499339718936e+42*cos(theta)**4 + 1.46192155319754e+41*cos(theta)**2 - 4.64102080380173e+38)*sin(26*phi)

#@torch.jit.script
def Yl36_m_minus_25(theta, phi):
    return 3.0227136881809e-38*(1.0 - cos(theta)**2)**12.5*(6.00102132103796e+43*cos(theta)**11 - 4.648678488128e+43*cos(theta)**9 + 1.21269873603339e+43*cos(theta)**7 - 1.26699867943787e+42*cos(theta)**5 + 4.87307184399181e+40*cos(theta)**3 - 4.64102080380173e+38*cos(theta))*sin(25*phi)

#@torch.jit.script
def Yl36_m_minus_24(theta, phi):
    return 8.17810257077045e-37*(1.0 - cos(theta)**2)**12*(5.00085110086497e+42*cos(theta)**12 - 4.648678488128e+42*cos(theta)**10 + 1.51587342004174e+42*cos(theta)**8 - 2.11166446572979e+41*cos(theta)**6 + 1.21826796099795e+40*cos(theta)**4 - 2.32051040190086e+38*cos(theta)**2 + 6.34019235492039e+35)*sin(24*phi)

#@torch.jit.script
def Yl36_m_minus_23(theta, phi):
    return 2.28401974801605e-35*(1.0 - cos(theta)**2)**11.5*(3.8468085391269e+41*cos(theta)**13 - 4.22607135284364e+41*cos(theta)**11 + 1.68430380004638e+41*cos(theta)**9 - 3.01666352247112e+40*cos(theta)**7 + 2.43653592199591e+39*cos(theta)**5 - 7.73503467300288e+37*cos(theta)**3 + 6.34019235492039e+35*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl36_m_minus_22(theta, phi):
    return 6.56432202813386e-34*(1.0 - cos(theta)**2)**11*(2.74772038509064e+40*cos(theta)**14 - 3.5217261273697e+40*cos(theta)**12 + 1.68430380004638e+40*cos(theta)**10 - 3.7708294030889e+39*cos(theta)**8 + 4.06089320332651e+38*cos(theta)**6 - 1.93375866825072e+37*cos(theta)**4 + 3.1700961774602e+35*cos(theta)**2 - 7.67577766939515e+32)*sin(22*phi)

#@torch.jit.script
def Yl36_m_minus_21(theta, phi):
    return 1.93619682908189e-32*(1.0 - cos(theta)**2)**10.5*(1.83181359006043e+39*cos(theta)**15 - 2.70902009797669e+39*cos(theta)**13 + 1.53118527276943e+39*cos(theta)**11 - 4.18981044787656e+38*cos(theta)**9 + 5.80127600475216e+37*cos(theta)**7 - 3.86751733650144e+36*cos(theta)**5 + 1.05669872582007e+35*cos(theta)**3 - 7.67577766939515e+32*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl36_m_minus_20(theta, phi):
    return 5.84718619746581e-31*(1.0 - cos(theta)**2)**10*(1.14488349378777e+38*cos(theta)**16 - 1.93501435569764e+38*cos(theta)**14 + 1.27598772730786e+38*cos(theta)**12 - 4.18981044787656e+37*cos(theta)**10 + 7.2515950059402e+36*cos(theta)**8 - 6.4458622275024e+35*cos(theta)**6 + 2.64174681455016e+34*cos(theta)**4 - 3.83788883469757e+32*cos(theta)**2 + 8.41642288310872e+29)*sin(20*phi)

#@torch.jit.script
def Yl36_m_minus_19(theta, phi):
    return 1.80411990397808e-29*(1.0 - cos(theta)**2)**9.5*(6.73460878698687e+36*cos(theta)**17 - 1.29000957046509e+37*cos(theta)**15 + 9.81529021006047e+36*cos(theta)**13 - 3.80891858897869e+36*cos(theta)**11 + 8.057327784378e+35*cos(theta)**9 - 9.20837461071771e+34*cos(theta)**7 + 5.28349362910033e+33*cos(theta)**5 - 1.27929627823252e+32*cos(theta)**3 + 8.41642288310872e+29*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl36_m_minus_18(theta, phi):
    return 5.67653075535627e-28*(1.0 - cos(theta)**2)**9*(3.74144932610382e+35*cos(theta)**18 - 8.06255981540682e+35*cos(theta)**16 + 7.01092157861462e+35*cos(theta)**14 - 3.17409882414891e+35*cos(theta)**12 + 8.057327784378e+34*cos(theta)**10 - 1.15104682633971e+34*cos(theta)**8 + 8.80582271516721e+32*cos(theta)**6 - 3.19824069558131e+31*cos(theta)**4 + 4.20821144155436e+29*cos(theta)**2 - 8.50143725566537e+26)*sin(18*phi)

#@torch.jit.script
def Yl36_m_minus_17(theta, phi):
    return 1.81826289225004e-26*(1.0 - cos(theta)**2)**8.5*(1.96918385584411e+34*cos(theta)**19 - 4.74268224435695e+34*cos(theta)**17 + 4.67394771907641e+34*cos(theta)**15 - 2.44161448011455e+34*cos(theta)**13 + 7.32484344034364e+33*cos(theta)**11 - 1.27894091815524e+33*cos(theta)**9 + 1.25797467359532e+32*cos(theta)**7 - 6.39648139116262e+30*cos(theta)**5 + 1.40273714718479e+29*cos(theta)**3 - 8.50143725566537e+26*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl36_m_minus_16(theta, phi):
    return 5.91983508389675e-25*(1.0 - cos(theta)**2)**8*(9.84591927922057e+32*cos(theta)**20 - 2.63482346908719e+33*cos(theta)**18 + 2.92121732442276e+33*cos(theta)**16 - 1.74401034293896e+33*cos(theta)**14 + 6.10403620028636e+32*cos(theta)**12 - 1.27894091815524e+32*cos(theta)**10 + 1.57246834199415e+31*cos(theta)**8 - 1.06608023186044e+30*cos(theta)**6 + 3.50684286796196e+28*cos(theta)**4 - 4.25071862783268e+26*cos(theta)**2 + 8.0202238260994e+23)*sin(16*phi)

#@torch.jit.script
def Yl36_m_minus_15(theta, phi):
    return 1.95623456117164e-23*(1.0 - cos(theta)**2)**7.5*(4.68853299010503e+31*cos(theta)**21 - 1.38674919425642e+32*cos(theta)**19 + 1.71836313201339e+32*cos(theta)**17 - 1.16267356195931e+32*cos(theta)**15 + 4.69541246175874e+31*cos(theta)**13 - 1.16267356195931e+31*cos(theta)**11 + 1.74718704666016e+30*cos(theta)**9 - 1.52297175980062e+29*cos(theta)**7 + 7.01368573592393e+27*cos(theta)**5 - 1.41690620927756e+26*cos(theta)**3 + 8.0202238260994e+23*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl36_m_minus_14(theta, phi):
    return 6.55265580099988e-22*(1.0 - cos(theta)**2)**7*(2.13115135913865e+30*cos(theta)**22 - 6.93374597128209e+30*cos(theta)**20 + 9.54646184451882e+30*cos(theta)**18 - 7.26670976224567e+30*cos(theta)**16 + 3.35386604411339e+30*cos(theta)**14 - 9.68894634966089e+29*cos(theta)**12 + 1.74718704666016e+29*cos(theta)**10 - 1.90371469975078e+28*cos(theta)**8 + 1.16894762265399e+27*cos(theta)**6 - 3.5422655231939e+25*cos(theta)**4 + 4.0101119130497e+23*cos(theta)**2 - 7.1481495776287e+20)*sin(14*phi)

#@torch.jit.script
def Yl36_m_minus_13(theta, phi):
    return 2.22211369541106e-20*(1.0 - cos(theta)**2)**6.5*(9.26587547451588e+28*cos(theta)**23 - 3.30178379584861e+29*cos(theta)**21 + 5.02445360237833e+29*cos(theta)**19 - 4.27453515426216e+29*cos(theta)**17 + 2.23591069607559e+29*cos(theta)**15 - 7.4530356535853e+28*cos(theta)**13 + 1.58835186060015e+28*cos(theta)**11 - 2.11523855527865e+27*cos(theta)**9 + 1.66992517521998e+26*cos(theta)**7 - 7.08453104638781e+24*cos(theta)**5 + 1.33670397101657e+23*cos(theta)**3 - 7.1481495776287e+20*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl36_m_minus_12(theta, phi):
    return 7.62026258589038e-19*(1.0 - cos(theta)**2)**6*(3.86078144771495e+27*cos(theta)**24 - 1.50081081629482e+28*cos(theta)**22 + 2.51222680118916e+28*cos(theta)**20 - 2.37474175236787e+28*cos(theta)**18 + 1.39744418504724e+28*cos(theta)**16 - 5.32359689541807e+27*cos(theta)**14 + 1.32362655050012e+27*cos(theta)**12 - 2.11523855527865e+26*cos(theta)**10 + 2.08740646902498e+25*cos(theta)**8 - 1.18075517439797e+24*cos(theta)**6 + 3.34175992754142e+22*cos(theta)**4 - 3.57407478881435e+20*cos(theta)**2 + 6.07835848437815e+17)*sin(12*phi)

#@torch.jit.script
def Yl36_m_minus_11(theta, phi):
    return 2.63973639315567e-17*(1.0 - cos(theta)**2)**5.5*(1.54431257908598e+26*cos(theta)**25 - 6.52526441867315e+26*cos(theta)**23 + 1.19629847675674e+27*cos(theta)**21 - 1.24986408019361e+27*cos(theta)**19 + 8.22025991204261e+26*cos(theta)**17 - 3.54906459694538e+26*cos(theta)**15 + 1.01817426961548e+26*cos(theta)**13 - 1.92294414116241e+25*cos(theta)**11 + 2.31934052113887e+24*cos(theta)**9 - 1.68679310628281e+23*cos(theta)**7 + 6.68351985508284e+21*cos(theta)**5 - 1.19135826293812e+20*cos(theta)**3 + 6.07835848437815e+17*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl36_m_minus_10(theta, phi):
    return 9.22775728515781e-16*(1.0 - cos(theta)**2)**5*(5.9396637657153e+24*cos(theta)**26 - 2.71886017444715e+25*cos(theta)**24 + 5.43772034889429e+25*cos(theta)**22 - 6.24932040096807e+25*cos(theta)**20 + 4.5668110622459e+25*cos(theta)**18 - 2.21816537309086e+25*cos(theta)**16 + 7.27267335439627e+24*cos(theta)**14 - 1.60245345096867e+24*cos(theta)**12 + 2.31934052113887e+23*cos(theta)**10 - 2.10849138285351e+22*cos(theta)**8 + 1.11391997584714e+21*cos(theta)**6 - 2.97839565734529e+19*cos(theta)**4 + 3.03917924218907e+17*cos(theta)**2 - 497410677936019.0)*sin(10*phi)

#@torch.jit.script
def Yl36_m_minus_9(theta, phi):
    return 3.25204810244434e-14*(1.0 - cos(theta)**2)**4.5*(2.19987546878345e+23*cos(theta)**27 - 1.08754406977886e+24*cos(theta)**25 + 2.36422623864969e+24*cos(theta)**23 - 2.97586685760384e+24*cos(theta)**21 + 2.4035847696031e+24*cos(theta)**19 - 1.30480316064168e+24*cos(theta)**17 + 4.84844890293085e+23*cos(theta)**15 - 1.23265650074513e+23*cos(theta)**13 + 2.10849138285351e+22*cos(theta)**11 - 2.34276820317057e+21*cos(theta)**9 + 1.5913142512102e+20*cos(theta)**7 - 5.95679131469059e+18*cos(theta)**5 + 1.01305974739636e+17*cos(theta)**3 - 497410677936019.0*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl36_m_minus_8(theta, phi):
    return 1.15436256195231e-12*(1.0 - cos(theta)**2)**4*(7.85669810279802e+21*cos(theta)**28 - 4.18286180684176e+22*cos(theta)**26 + 9.85094266104039e+22*cos(theta)**24 - 1.35266675345629e+23*cos(theta)**22 + 1.20179238480155e+23*cos(theta)**20 - 7.24890644800936e+22*cos(theta)**18 + 3.03028056433178e+22*cos(theta)**16 - 8.80468929103665e+21*cos(theta)**14 + 1.75707615237793e+21*cos(theta)**12 - 2.34276820317057e+20*cos(theta)**10 + 1.98914281401275e+19*cos(theta)**8 - 9.92798552448431e+17*cos(theta)**6 + 2.5326493684909e+16*cos(theta)**4 - 248705338968009.0*cos(theta)**2 + 394770379314.301)*sin(8*phi)

#@torch.jit.script
def Yl36_m_minus_7(theta, phi):
    return 4.12351492246812e-11*(1.0 - cos(theta)**2)**3.5*(2.70920624234415e+20*cos(theta)**29 - 1.54920807660806e+21*cos(theta)**27 + 3.94037706441615e+21*cos(theta)**25 - 5.88115979763605e+21*cos(theta)**23 + 5.72282088000739e+21*cos(theta)**21 - 3.81521392000493e+21*cos(theta)**19 + 1.78251797901869e+21*cos(theta)**17 - 5.8697928606911e+20*cos(theta)**15 + 1.35159704029071e+20*cos(theta)**13 - 2.12978927560961e+19*cos(theta)**11 + 2.21015868223639e+18*cos(theta)**9 - 1.4182836463549e+17*cos(theta)**7 + 5.06529873698179e+15*cos(theta)**5 - 82901779656003.1*cos(theta)**3 + 394770379314.301*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl36_m_minus_6(theta, phi):
    return 1.48102512326443e-9*(1.0 - cos(theta)**2)**3*(9.03068747448049e+18*cos(theta)**30 - 5.53288598788593e+19*cos(theta)**28 + 1.51552964016006e+20*cos(theta)**26 - 2.45048324901502e+20*cos(theta)**24 + 2.60128221818518e+20*cos(theta)**22 - 1.90760696000246e+20*cos(theta)**20 + 9.90287766121497e+19*cos(theta)**18 - 3.66862053793194e+19*cos(theta)**16 + 9.6542645735051e+18*cos(theta)**14 - 1.77482439634134e+18*cos(theta)**12 + 2.21015868223639e+17*cos(theta)**10 - 1.77285455794363e+16*cos(theta)**8 + 844216456163632.0*cos(theta)**6 - 20725444914000.8*cos(theta)**4 + 197385189657.15*cos(theta)**2 - 306023549.856047)*sin(6*phi)

#@torch.jit.script
def Yl36_m_minus_5(theta, phi):
    return 5.34401806817122e-8*(1.0 - cos(theta)**2)**2.5*(2.9131249917679e+17*cos(theta)**31 - 1.90789171996067e+18*cos(theta)**29 + 5.61307274133355e+18*cos(theta)**27 - 9.80193299606009e+18*cos(theta)**25 + 1.13099226877616e+19*cos(theta)**23 - 9.08384266667839e+18*cos(theta)**21 + 5.21204087432367e+18*cos(theta)**19 - 2.15801208113643e+18*cos(theta)**17 + 6.43617638233673e+17*cos(theta)**15 - 1.36524953564719e+17*cos(theta)**13 + 2.00923516566944e+16*cos(theta)**11 - 1.96983839771514e+15*cos(theta)**9 + 120602350880519.0*cos(theta)**7 - 4145088982800.16*cos(theta)**5 + 65795063219.0501*cos(theta)**3 - 306023549.856047*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl36_m_minus_4(theta, phi):
    return 1.93568567169822e-6*(1.0 - cos(theta)**2)**2*(9.10351559927468e+15*cos(theta)**32 - 6.35963906653555e+16*cos(theta)**30 + 2.00466883619055e+17*cos(theta)**28 - 3.76997422925388e+17*cos(theta)**26 + 4.71246778656735e+17*cos(theta)**24 - 4.12901939394473e+17*cos(theta)**22 + 2.60602043716183e+17*cos(theta)**20 - 1.19889560063135e+17*cos(theta)**18 + 4.02261023896046e+16*cos(theta)**16 - 9.7517823974799e+15*cos(theta)**14 + 1.67436263805787e+15*cos(theta)**12 - 196983839771514.0*cos(theta)**10 + 15075293860064.9*cos(theta)**8 - 690848163800.026*cos(theta)**6 + 16448765804.7625*cos(theta)**4 - 153011774.928023*cos(theta)**2 + 233249.656902475)*sin(4*phi)

#@torch.jit.script
def Yl36_m_minus_3(theta, phi):
    return 7.03269529120626e-5*(1.0 - cos(theta)**2)**1.5*(275864109068930.0*cos(theta)**33 - 2.05149647307599e+15*cos(theta)**31 + 6.91265115927778e+15*cos(theta)**29 - 1.39628675157551e+16*cos(theta)**27 + 1.88498711462694e+16*cos(theta)**25 - 1.79522582345423e+16*cos(theta)**23 + 1.24096211293421e+16*cos(theta)**21 - 6.30997684542817e+15*cos(theta)**19 + 2.36624131703556e+15*cos(theta)**17 - 650118826498660.0*cos(theta)**15 + 128797126004452.0*cos(theta)**13 - 17907621797410.4*cos(theta)**11 + 1675032651118.32*cos(theta)**9 - 98692594828.5751*cos(theta)**7 + 3289753160.9525*cos(theta)**5 - 51003924.9760078*cos(theta)**3 + 233249.656902475*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl36_m_minus_2(theta, phi):
    return 0.00256090555968341*(1.0 - cos(theta)**2)*(8113650266733.23*cos(theta)**34 - 64109264783624.5*cos(theta)**32 + 230421705309259.0*cos(theta)**30 - 498673839848397.0*cos(theta)**28 + 724995044087285.0*cos(theta)**26 - 748010759772595.0*cos(theta)**24 + 564073687697367.0*cos(theta)**22 - 315498842271409.0*cos(theta)**20 + 131457850946420.0*cos(theta)**18 - 40632426656166.3*cos(theta)**16 + 9199794714603.68*cos(theta)**14 - 1492301816450.86*cos(theta)**12 + 167503265111.832*cos(theta)**10 - 12336574353.5719*cos(theta)**8 + 548292193.492084*cos(theta)**6 - 12750981.244002*cos(theta)**4 + 116624.828451237*cos(theta)**2 - 175.904718629317)*sin(2*phi)

#@torch.jit.script
def Yl36_m_minus_1(theta, phi):
    return 0.0933940875530734*(1.0 - cos(theta)**2)**0.5*(231818579049.521*cos(theta)**35 - 1942704993443.17*cos(theta)**33 + 7432958235782.55*cos(theta)**31 - 17195649649944.7*cos(theta)**29 + 26851668299529.1*cos(theta)**27 - 29920430390903.8*cos(theta)**25 + 24524942943363.8*cos(theta)**23 - 15023754393876.6*cos(theta)**21 + 6918834260337.91*cos(theta)**19 - 2390142744480.37*cos(theta)**17 + 613319647640.245*cos(theta)**15 - 114792447419.297*cos(theta)**13 + 15227569555.6211*cos(theta)**11 - 1370730483.73021*cos(theta)**9 + 78327456.2131549*cos(theta)**7 - 2550196.24880039*cos(theta)**5 + 38874.9428170791*cos(theta)**3 - 175.904718629317*cos(theta))*sin(phi)

#@torch.jit.script
def Yl36_m0(theta, phi):
    return 48758699040.5494*cos(theta)**36 - 432647611204.875*cos(theta)**34 + 1758806593376.34*cos(theta)**32 - 4340139653306.79*cos(theta)**30 + 7261387496878.67*cos(theta)**28 - 8713664996254.4*cos(theta)**26 + 7737544054051.04*cos(theta)**24 - 5170852685031.69*cos(theta)**22 + 2619445110180.53*cos(theta)**20 - 1005443577645.05*cos(theta)**18 + 290250693169.232*cos(theta)**16 - 62085709768.8196*cos(theta)**14 + 9608502702.31732*cos(theta)**12 - 1037907002.21431*cos(theta)**10 + 74136214.4438792*cos(theta)**8 - 3218316.28593584*cos(theta)**6 + 73589.549221094*cos(theta)**4 - 665.96877123162*cos(theta)**2 + 0.999953109957387

#@torch.jit.script
def Yl36_m1(theta, phi):
    return 0.0933940875530734*(1.0 - cos(theta)**2)**0.5*(231818579049.521*cos(theta)**35 - 1942704993443.17*cos(theta)**33 + 7432958235782.55*cos(theta)**31 - 17195649649944.7*cos(theta)**29 + 26851668299529.1*cos(theta)**27 - 29920430390903.8*cos(theta)**25 + 24524942943363.8*cos(theta)**23 - 15023754393876.6*cos(theta)**21 + 6918834260337.91*cos(theta)**19 - 2390142744480.37*cos(theta)**17 + 613319647640.245*cos(theta)**15 - 114792447419.297*cos(theta)**13 + 15227569555.6211*cos(theta)**11 - 1370730483.73021*cos(theta)**9 + 78327456.2131549*cos(theta)**7 - 2550196.24880039*cos(theta)**5 + 38874.9428170791*cos(theta)**3 - 175.904718629317*cos(theta))*cos(phi)

#@torch.jit.script
def Yl36_m2(theta, phi):
    return 0.00256090555968341*(1.0 - cos(theta)**2)*(8113650266733.23*cos(theta)**34 - 64109264783624.5*cos(theta)**32 + 230421705309259.0*cos(theta)**30 - 498673839848397.0*cos(theta)**28 + 724995044087285.0*cos(theta)**26 - 748010759772595.0*cos(theta)**24 + 564073687697367.0*cos(theta)**22 - 315498842271409.0*cos(theta)**20 + 131457850946420.0*cos(theta)**18 - 40632426656166.3*cos(theta)**16 + 9199794714603.68*cos(theta)**14 - 1492301816450.86*cos(theta)**12 + 167503265111.832*cos(theta)**10 - 12336574353.5719*cos(theta)**8 + 548292193.492084*cos(theta)**6 - 12750981.244002*cos(theta)**4 + 116624.828451237*cos(theta)**2 - 175.904718629317)*cos(2*phi)

#@torch.jit.script
def Yl36_m3(theta, phi):
    return 7.03269529120626e-5*(1.0 - cos(theta)**2)**1.5*(275864109068930.0*cos(theta)**33 - 2.05149647307599e+15*cos(theta)**31 + 6.91265115927778e+15*cos(theta)**29 - 1.39628675157551e+16*cos(theta)**27 + 1.88498711462694e+16*cos(theta)**25 - 1.79522582345423e+16*cos(theta)**23 + 1.24096211293421e+16*cos(theta)**21 - 6.30997684542817e+15*cos(theta)**19 + 2.36624131703556e+15*cos(theta)**17 - 650118826498660.0*cos(theta)**15 + 128797126004452.0*cos(theta)**13 - 17907621797410.4*cos(theta)**11 + 1675032651118.32*cos(theta)**9 - 98692594828.5751*cos(theta)**7 + 3289753160.9525*cos(theta)**5 - 51003924.9760078*cos(theta)**3 + 233249.656902475*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl36_m4(theta, phi):
    return 1.93568567169822e-6*(1.0 - cos(theta)**2)**2*(9.10351559927468e+15*cos(theta)**32 - 6.35963906653555e+16*cos(theta)**30 + 2.00466883619055e+17*cos(theta)**28 - 3.76997422925388e+17*cos(theta)**26 + 4.71246778656735e+17*cos(theta)**24 - 4.12901939394473e+17*cos(theta)**22 + 2.60602043716183e+17*cos(theta)**20 - 1.19889560063135e+17*cos(theta)**18 + 4.02261023896046e+16*cos(theta)**16 - 9.7517823974799e+15*cos(theta)**14 + 1.67436263805787e+15*cos(theta)**12 - 196983839771514.0*cos(theta)**10 + 15075293860064.9*cos(theta)**8 - 690848163800.026*cos(theta)**6 + 16448765804.7625*cos(theta)**4 - 153011774.928023*cos(theta)**2 + 233249.656902475)*cos(4*phi)

#@torch.jit.script
def Yl36_m5(theta, phi):
    return 5.34401806817122e-8*(1.0 - cos(theta)**2)**2.5*(2.9131249917679e+17*cos(theta)**31 - 1.90789171996067e+18*cos(theta)**29 + 5.61307274133355e+18*cos(theta)**27 - 9.80193299606009e+18*cos(theta)**25 + 1.13099226877616e+19*cos(theta)**23 - 9.08384266667839e+18*cos(theta)**21 + 5.21204087432367e+18*cos(theta)**19 - 2.15801208113643e+18*cos(theta)**17 + 6.43617638233673e+17*cos(theta)**15 - 1.36524953564719e+17*cos(theta)**13 + 2.00923516566944e+16*cos(theta)**11 - 1.96983839771514e+15*cos(theta)**9 + 120602350880519.0*cos(theta)**7 - 4145088982800.16*cos(theta)**5 + 65795063219.0501*cos(theta)**3 - 306023549.856047*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl36_m6(theta, phi):
    return 1.48102512326443e-9*(1.0 - cos(theta)**2)**3*(9.03068747448049e+18*cos(theta)**30 - 5.53288598788593e+19*cos(theta)**28 + 1.51552964016006e+20*cos(theta)**26 - 2.45048324901502e+20*cos(theta)**24 + 2.60128221818518e+20*cos(theta)**22 - 1.90760696000246e+20*cos(theta)**20 + 9.90287766121497e+19*cos(theta)**18 - 3.66862053793194e+19*cos(theta)**16 + 9.6542645735051e+18*cos(theta)**14 - 1.77482439634134e+18*cos(theta)**12 + 2.21015868223639e+17*cos(theta)**10 - 1.77285455794363e+16*cos(theta)**8 + 844216456163632.0*cos(theta)**6 - 20725444914000.8*cos(theta)**4 + 197385189657.15*cos(theta)**2 - 306023549.856047)*cos(6*phi)

#@torch.jit.script
def Yl36_m7(theta, phi):
    return 4.12351492246812e-11*(1.0 - cos(theta)**2)**3.5*(2.70920624234415e+20*cos(theta)**29 - 1.54920807660806e+21*cos(theta)**27 + 3.94037706441615e+21*cos(theta)**25 - 5.88115979763605e+21*cos(theta)**23 + 5.72282088000739e+21*cos(theta)**21 - 3.81521392000493e+21*cos(theta)**19 + 1.78251797901869e+21*cos(theta)**17 - 5.8697928606911e+20*cos(theta)**15 + 1.35159704029071e+20*cos(theta)**13 - 2.12978927560961e+19*cos(theta)**11 + 2.21015868223639e+18*cos(theta)**9 - 1.4182836463549e+17*cos(theta)**7 + 5.06529873698179e+15*cos(theta)**5 - 82901779656003.1*cos(theta)**3 + 394770379314.301*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl36_m8(theta, phi):
    return 1.15436256195231e-12*(1.0 - cos(theta)**2)**4*(7.85669810279802e+21*cos(theta)**28 - 4.18286180684176e+22*cos(theta)**26 + 9.85094266104039e+22*cos(theta)**24 - 1.35266675345629e+23*cos(theta)**22 + 1.20179238480155e+23*cos(theta)**20 - 7.24890644800936e+22*cos(theta)**18 + 3.03028056433178e+22*cos(theta)**16 - 8.80468929103665e+21*cos(theta)**14 + 1.75707615237793e+21*cos(theta)**12 - 2.34276820317057e+20*cos(theta)**10 + 1.98914281401275e+19*cos(theta)**8 - 9.92798552448431e+17*cos(theta)**6 + 2.5326493684909e+16*cos(theta)**4 - 248705338968009.0*cos(theta)**2 + 394770379314.301)*cos(8*phi)

#@torch.jit.script
def Yl36_m9(theta, phi):
    return 3.25204810244434e-14*(1.0 - cos(theta)**2)**4.5*(2.19987546878345e+23*cos(theta)**27 - 1.08754406977886e+24*cos(theta)**25 + 2.36422623864969e+24*cos(theta)**23 - 2.97586685760384e+24*cos(theta)**21 + 2.4035847696031e+24*cos(theta)**19 - 1.30480316064168e+24*cos(theta)**17 + 4.84844890293085e+23*cos(theta)**15 - 1.23265650074513e+23*cos(theta)**13 + 2.10849138285351e+22*cos(theta)**11 - 2.34276820317057e+21*cos(theta)**9 + 1.5913142512102e+20*cos(theta)**7 - 5.95679131469059e+18*cos(theta)**5 + 1.01305974739636e+17*cos(theta)**3 - 497410677936019.0*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl36_m10(theta, phi):
    return 9.22775728515781e-16*(1.0 - cos(theta)**2)**5*(5.9396637657153e+24*cos(theta)**26 - 2.71886017444715e+25*cos(theta)**24 + 5.43772034889429e+25*cos(theta)**22 - 6.24932040096807e+25*cos(theta)**20 + 4.5668110622459e+25*cos(theta)**18 - 2.21816537309086e+25*cos(theta)**16 + 7.27267335439627e+24*cos(theta)**14 - 1.60245345096867e+24*cos(theta)**12 + 2.31934052113887e+23*cos(theta)**10 - 2.10849138285351e+22*cos(theta)**8 + 1.11391997584714e+21*cos(theta)**6 - 2.97839565734529e+19*cos(theta)**4 + 3.03917924218907e+17*cos(theta)**2 - 497410677936019.0)*cos(10*phi)

#@torch.jit.script
def Yl36_m11(theta, phi):
    return 2.63973639315567e-17*(1.0 - cos(theta)**2)**5.5*(1.54431257908598e+26*cos(theta)**25 - 6.52526441867315e+26*cos(theta)**23 + 1.19629847675674e+27*cos(theta)**21 - 1.24986408019361e+27*cos(theta)**19 + 8.22025991204261e+26*cos(theta)**17 - 3.54906459694538e+26*cos(theta)**15 + 1.01817426961548e+26*cos(theta)**13 - 1.92294414116241e+25*cos(theta)**11 + 2.31934052113887e+24*cos(theta)**9 - 1.68679310628281e+23*cos(theta)**7 + 6.68351985508284e+21*cos(theta)**5 - 1.19135826293812e+20*cos(theta)**3 + 6.07835848437815e+17*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl36_m12(theta, phi):
    return 7.62026258589038e-19*(1.0 - cos(theta)**2)**6*(3.86078144771495e+27*cos(theta)**24 - 1.50081081629482e+28*cos(theta)**22 + 2.51222680118916e+28*cos(theta)**20 - 2.37474175236787e+28*cos(theta)**18 + 1.39744418504724e+28*cos(theta)**16 - 5.32359689541807e+27*cos(theta)**14 + 1.32362655050012e+27*cos(theta)**12 - 2.11523855527865e+26*cos(theta)**10 + 2.08740646902498e+25*cos(theta)**8 - 1.18075517439797e+24*cos(theta)**6 + 3.34175992754142e+22*cos(theta)**4 - 3.57407478881435e+20*cos(theta)**2 + 6.07835848437815e+17)*cos(12*phi)

#@torch.jit.script
def Yl36_m13(theta, phi):
    return 2.22211369541106e-20*(1.0 - cos(theta)**2)**6.5*(9.26587547451588e+28*cos(theta)**23 - 3.30178379584861e+29*cos(theta)**21 + 5.02445360237833e+29*cos(theta)**19 - 4.27453515426216e+29*cos(theta)**17 + 2.23591069607559e+29*cos(theta)**15 - 7.4530356535853e+28*cos(theta)**13 + 1.58835186060015e+28*cos(theta)**11 - 2.11523855527865e+27*cos(theta)**9 + 1.66992517521998e+26*cos(theta)**7 - 7.08453104638781e+24*cos(theta)**5 + 1.33670397101657e+23*cos(theta)**3 - 7.1481495776287e+20*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl36_m14(theta, phi):
    return 6.55265580099988e-22*(1.0 - cos(theta)**2)**7*(2.13115135913865e+30*cos(theta)**22 - 6.93374597128209e+30*cos(theta)**20 + 9.54646184451882e+30*cos(theta)**18 - 7.26670976224567e+30*cos(theta)**16 + 3.35386604411339e+30*cos(theta)**14 - 9.68894634966089e+29*cos(theta)**12 + 1.74718704666016e+29*cos(theta)**10 - 1.90371469975078e+28*cos(theta)**8 + 1.16894762265399e+27*cos(theta)**6 - 3.5422655231939e+25*cos(theta)**4 + 4.0101119130497e+23*cos(theta)**2 - 7.1481495776287e+20)*cos(14*phi)

#@torch.jit.script
def Yl36_m15(theta, phi):
    return 1.95623456117164e-23*(1.0 - cos(theta)**2)**7.5*(4.68853299010503e+31*cos(theta)**21 - 1.38674919425642e+32*cos(theta)**19 + 1.71836313201339e+32*cos(theta)**17 - 1.16267356195931e+32*cos(theta)**15 + 4.69541246175874e+31*cos(theta)**13 - 1.16267356195931e+31*cos(theta)**11 + 1.74718704666016e+30*cos(theta)**9 - 1.52297175980062e+29*cos(theta)**7 + 7.01368573592393e+27*cos(theta)**5 - 1.41690620927756e+26*cos(theta)**3 + 8.0202238260994e+23*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl36_m16(theta, phi):
    return 5.91983508389675e-25*(1.0 - cos(theta)**2)**8*(9.84591927922057e+32*cos(theta)**20 - 2.63482346908719e+33*cos(theta)**18 + 2.92121732442276e+33*cos(theta)**16 - 1.74401034293896e+33*cos(theta)**14 + 6.10403620028636e+32*cos(theta)**12 - 1.27894091815524e+32*cos(theta)**10 + 1.57246834199415e+31*cos(theta)**8 - 1.06608023186044e+30*cos(theta)**6 + 3.50684286796196e+28*cos(theta)**4 - 4.25071862783268e+26*cos(theta)**2 + 8.0202238260994e+23)*cos(16*phi)

#@torch.jit.script
def Yl36_m17(theta, phi):
    return 1.81826289225004e-26*(1.0 - cos(theta)**2)**8.5*(1.96918385584411e+34*cos(theta)**19 - 4.74268224435695e+34*cos(theta)**17 + 4.67394771907641e+34*cos(theta)**15 - 2.44161448011455e+34*cos(theta)**13 + 7.32484344034364e+33*cos(theta)**11 - 1.27894091815524e+33*cos(theta)**9 + 1.25797467359532e+32*cos(theta)**7 - 6.39648139116262e+30*cos(theta)**5 + 1.40273714718479e+29*cos(theta)**3 - 8.50143725566537e+26*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl36_m18(theta, phi):
    return 5.67653075535627e-28*(1.0 - cos(theta)**2)**9*(3.74144932610382e+35*cos(theta)**18 - 8.06255981540682e+35*cos(theta)**16 + 7.01092157861462e+35*cos(theta)**14 - 3.17409882414891e+35*cos(theta)**12 + 8.057327784378e+34*cos(theta)**10 - 1.15104682633971e+34*cos(theta)**8 + 8.80582271516721e+32*cos(theta)**6 - 3.19824069558131e+31*cos(theta)**4 + 4.20821144155436e+29*cos(theta)**2 - 8.50143725566537e+26)*cos(18*phi)

#@torch.jit.script
def Yl36_m19(theta, phi):
    return 1.80411990397808e-29*(1.0 - cos(theta)**2)**9.5*(6.73460878698687e+36*cos(theta)**17 - 1.29000957046509e+37*cos(theta)**15 + 9.81529021006047e+36*cos(theta)**13 - 3.80891858897869e+36*cos(theta)**11 + 8.057327784378e+35*cos(theta)**9 - 9.20837461071771e+34*cos(theta)**7 + 5.28349362910033e+33*cos(theta)**5 - 1.27929627823252e+32*cos(theta)**3 + 8.41642288310872e+29*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl36_m20(theta, phi):
    return 5.84718619746581e-31*(1.0 - cos(theta)**2)**10*(1.14488349378777e+38*cos(theta)**16 - 1.93501435569764e+38*cos(theta)**14 + 1.27598772730786e+38*cos(theta)**12 - 4.18981044787656e+37*cos(theta)**10 + 7.2515950059402e+36*cos(theta)**8 - 6.4458622275024e+35*cos(theta)**6 + 2.64174681455016e+34*cos(theta)**4 - 3.83788883469757e+32*cos(theta)**2 + 8.41642288310872e+29)*cos(20*phi)

#@torch.jit.script
def Yl36_m21(theta, phi):
    return 1.93619682908189e-32*(1.0 - cos(theta)**2)**10.5*(1.83181359006043e+39*cos(theta)**15 - 2.70902009797669e+39*cos(theta)**13 + 1.53118527276943e+39*cos(theta)**11 - 4.18981044787656e+38*cos(theta)**9 + 5.80127600475216e+37*cos(theta)**7 - 3.86751733650144e+36*cos(theta)**5 + 1.05669872582007e+35*cos(theta)**3 - 7.67577766939515e+32*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl36_m22(theta, phi):
    return 6.56432202813386e-34*(1.0 - cos(theta)**2)**11*(2.74772038509064e+40*cos(theta)**14 - 3.5217261273697e+40*cos(theta)**12 + 1.68430380004638e+40*cos(theta)**10 - 3.7708294030889e+39*cos(theta)**8 + 4.06089320332651e+38*cos(theta)**6 - 1.93375866825072e+37*cos(theta)**4 + 3.1700961774602e+35*cos(theta)**2 - 7.67577766939515e+32)*cos(22*phi)

#@torch.jit.script
def Yl36_m23(theta, phi):
    return 2.28401974801605e-35*(1.0 - cos(theta)**2)**11.5*(3.8468085391269e+41*cos(theta)**13 - 4.22607135284364e+41*cos(theta)**11 + 1.68430380004638e+41*cos(theta)**9 - 3.01666352247112e+40*cos(theta)**7 + 2.43653592199591e+39*cos(theta)**5 - 7.73503467300288e+37*cos(theta)**3 + 6.34019235492039e+35*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl36_m24(theta, phi):
    return 8.17810257077045e-37*(1.0 - cos(theta)**2)**12*(5.00085110086497e+42*cos(theta)**12 - 4.648678488128e+42*cos(theta)**10 + 1.51587342004174e+42*cos(theta)**8 - 2.11166446572979e+41*cos(theta)**6 + 1.21826796099795e+40*cos(theta)**4 - 2.32051040190086e+38*cos(theta)**2 + 6.34019235492039e+35)*cos(24*phi)

#@torch.jit.script
def Yl36_m25(theta, phi):
    return 3.0227136881809e-38*(1.0 - cos(theta)**2)**12.5*(6.00102132103796e+43*cos(theta)**11 - 4.648678488128e+43*cos(theta)**9 + 1.21269873603339e+43*cos(theta)**7 - 1.26699867943787e+42*cos(theta)**5 + 4.87307184399181e+40*cos(theta)**3 - 4.64102080380173e+38*cos(theta))*cos(25*phi)

#@torch.jit.script
def Yl36_m26(theta, phi):
    return 1.1574568923217e-39*(1.0 - cos(theta)**2)**13*(6.60112345314176e+44*cos(theta)**10 - 4.1838106393152e+44*cos(theta)**8 + 8.48889115223374e+43*cos(theta)**6 - 6.33499339718936e+42*cos(theta)**4 + 1.46192155319754e+41*cos(theta)**2 - 4.64102080380173e+38)*cos(26*phi)

#@torch.jit.script
def Yl36_m27(theta, phi):
    return 4.61141863924726e-41*(1.0 - cos(theta)**2)**13.5*(6.60112345314176e+45*cos(theta)**9 - 3.34704851145216e+45*cos(theta)**7 + 5.09333469134024e+44*cos(theta)**5 - 2.53399735887574e+43*cos(theta)**3 + 2.92384310639509e+41*cos(theta))*cos(27*phi)

#@torch.jit.script
def Yl36_m28(theta, phi):
    return 1.92142443301969e-42*(1.0 - cos(theta)**2)**14*(5.94101110782758e+46*cos(theta)**8 - 2.34293395801651e+46*cos(theta)**6 + 2.54666734567012e+45*cos(theta)**4 - 7.60199207662723e+43*cos(theta)**2 + 2.92384310639509e+41)*cos(28*phi)

#@torch.jit.script
def Yl36_m29(theta, phi):
    return 8.42600353736191e-44*(1.0 - cos(theta)**2)**14.5*(4.75280888626207e+47*cos(theta)**7 - 1.40576037480991e+47*cos(theta)**5 + 1.01866693826805e+46*cos(theta)**3 - 1.52039841532545e+44*cos(theta))*cos(29*phi)

#@torch.jit.script
def Yl36_m30(theta, phi):
    return 3.92013162413846e-45*(1.0 - cos(theta)**2)**15*(3.32696622038345e+48*cos(theta)**6 - 7.02880187404954e+47*cos(theta)**4 + 3.05600081480415e+46*cos(theta)**2 - 1.52039841532545e+44)*cos(30*phi)

#@torch.jit.script
def Yl36_m31(theta, phi):
    return 1.95518394692445e-46*(1.0 - cos(theta)**2)**15.5*(1.99617973223007e+49*cos(theta)**5 - 2.81152074961981e+48*cos(theta)**3 + 6.11200162960829e+46*cos(theta))*cos(31*phi)

#@torch.jit.script
def Yl36_m32(theta, phi):
    return 1.06034737181502e-47*(1.0 - cos(theta)**2)**16*(9.98089866115034e+49*cos(theta)**4 - 8.43456224885944e+48*cos(theta)**2 + 6.11200162960829e+46)*cos(32*phi)

#@torch.jit.script
def Yl36_m33(theta, phi):
    return 6.38254114616021e-49*(1.0 - cos(theta)**2)**16.5*(3.99235946446014e+50*cos(theta)**3 - 1.68691244977189e+49*cos(theta))*cos(33*phi)

#@torch.jit.script
def Yl36_m34(theta, phi):
    return 4.40437182605064e-50*(1.0 - cos(theta)**2)**17*(1.19770783933804e+51*cos(theta)**2 - 1.68691244977189e+49)*cos(34*phi)

#@torch.jit.script
def Yl36_m35(theta, phi):
    return 8.85361619789771*(1.0 - cos(theta)**2)**17.5*cos(35*phi)*cos(theta)

#@torch.jit.script
def Yl36_m36(theta, phi):
    return 1.04340867525942*(1.0 - cos(theta)**2)**18*cos(36*phi)

#@torch.jit.script
def Yl37_m_minus_37(theta, phi):
    return 1.05043507569481*(1.0 - cos(theta)**2)**18.5*sin(37*phi)

#@torch.jit.script
def Yl37_m_minus_36(theta, phi):
    return 9.03618419303727*(1.0 - cos(theta)**2)**18*sin(36*phi)*cos(theta)

#@torch.jit.script
def Yl37_m_minus_35(theta, phi):
    return 6.24392610871321e-52*(1.0 - cos(theta)**2)**17.5*(8.7432672271677e+52*cos(theta)**2 - 1.19770783933804e+51)*sin(35*phi)

#@torch.jit.script
def Yl37_m_minus_34(theta, phi):
    return 9.17665977479345e-51*(1.0 - cos(theta)**2)**17*(2.9144224090559e+52*cos(theta)**3 - 1.19770783933804e+51*cos(theta))*sin(34*phi)

#@torch.jit.script
def Yl37_m_minus_33(theta, phi):
    return 1.54647819359785e-49*(1.0 - cos(theta)**2)**16.5*(7.28605602263975e+51*cos(theta)**4 - 5.98853919669021e+50*cos(theta)**2 + 4.21728112442972e+48)*sin(33*phi)

#@torch.jit.script
def Yl37_m_minus_32(theta, phi):
    return 2.89319577828011e-48*(1.0 - cos(theta)**2)**16*(1.45721120452795e+51*cos(theta)**5 - 1.99617973223007e+50*cos(theta)**3 + 4.21728112442972e+48*cos(theta))*sin(32*phi)

#@torch.jit.script
def Yl37_m_minus_31(theta, phi):
    return 5.88678254222418e-47*(1.0 - cos(theta)**2)**15.5*(2.42868534087992e+50*cos(theta)**6 - 4.99044933057517e+49*cos(theta)**4 + 2.10864056221486e+48*cos(theta)**2 - 1.01866693826805e+46)*sin(31*phi)

#@torch.jit.script
def Yl37_m_minus_30(theta, phi):
    return 1.28434432069174e-45*(1.0 - cos(theta)**2)**15*(3.46955048697131e+49*cos(theta)**7 - 9.98089866115034e+48*cos(theta)**5 + 7.02880187404954e+47*cos(theta)**3 - 1.01866693826805e+46*cos(theta))*sin(30*phi)

#@torch.jit.script
def Yl37_m_minus_29(theta, phi):
    return 2.9734720766705e-44*(1.0 - cos(theta)**2)**14.5*(4.33693810871414e+48*cos(theta)**8 - 1.66348311019172e+48*cos(theta)**6 + 1.75720046851238e+47*cos(theta)**4 - 5.09333469134024e+45*cos(theta)**2 + 1.90049801915681e+43)*sin(29*phi)

#@torch.jit.script
def Yl37_m_minus_28(theta, phi):
    return 7.24698040379513e-43*(1.0 - cos(theta)**2)**14*(4.81882012079349e+47*cos(theta)**9 - 2.37640444313103e+47*cos(theta)**7 + 3.51440093702477e+46*cos(theta)**5 - 1.69777823044675e+45*cos(theta)**3 + 1.90049801915681e+43*cos(theta))*sin(28*phi)

#@torch.jit.script
def Yl37_m_minus_27(theta, phi):
    return 1.84762472467879e-41*(1.0 - cos(theta)**2)**13.5*(4.81882012079349e+46*cos(theta)**10 - 2.97050555391379e+46*cos(theta)**8 + 5.85733489504128e+45*cos(theta)**6 - 4.24444557611687e+44*cos(theta)**4 + 9.50249009578404e+42*cos(theta)**2 - 2.92384310639509e+40)*sin(27*phi)

#@torch.jit.script
def Yl37_m_minus_26(theta, phi):
    return 4.90230237211461e-40*(1.0 - cos(theta)**2)**13*(4.38074556435771e+45*cos(theta)**11 - 3.30056172657088e+45*cos(theta)**9 + 8.3676212786304e+44*cos(theta)**7 - 8.48889115223374e+43*cos(theta)**5 + 3.16749669859468e+42*cos(theta)**3 - 2.92384310639509e+40*cos(theta))*sin(26*phi)

#@torch.jit.script
def Yl37_m_minus_25(theta, phi):
    return 1.34791030198661e-38*(1.0 - cos(theta)**2)**12.5*(3.65062130363143e+44*cos(theta)**12 - 3.30056172657088e+44*cos(theta)**10 + 1.0459526598288e+44*cos(theta)**8 - 1.41481519203896e+43*cos(theta)**6 + 7.9187417464867e+41*cos(theta)**4 - 1.46192155319754e+40*cos(theta)**2 + 3.86751733650144e+37)*sin(25*phi)

#@torch.jit.script
def Yl37_m_minus_24(theta, phi):
    return 3.82673610124151e-37*(1.0 - cos(theta)**2)**12*(2.80817023356264e+43*cos(theta)**13 - 3.00051066051898e+43*cos(theta)**11 + 1.162169622032e+43*cos(theta)**9 - 2.02116456005565e+42*cos(theta)**7 + 1.58374834929734e+41*cos(theta)**5 - 4.87307184399181e+39*cos(theta)**3 + 3.86751733650144e+37*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl37_m_minus_23(theta, phi):
    return 1.11829774420847e-35*(1.0 - cos(theta)**2)**11.5*(2.00583588111617e+42*cos(theta)**14 - 2.50042555043248e+42*cos(theta)**12 + 1.162169622032e+42*cos(theta)**10 - 2.52645570006957e+41*cos(theta)**8 + 2.63958058216223e+40*cos(theta)**6 - 1.21826796099795e+39*cos(theta)**4 + 1.93375866825072e+37*cos(theta)**2 - 4.52870882494314e+34)*sin(23*phi)

#@torch.jit.script
def Yl37_m_minus_22(theta, phi):
    return 3.3548932326254e-34*(1.0 - cos(theta)**2)**11*(1.33722392074411e+41*cos(theta)**15 - 1.92340426956345e+41*cos(theta)**13 + 1.05651783821091e+41*cos(theta)**11 - 2.80717300007729e+40*cos(theta)**9 + 3.7708294030889e+39*cos(theta)**7 - 2.43653592199591e+38*cos(theta)**5 + 6.4458622275024e+36*cos(theta)**3 - 4.52870882494314e+34*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl37_m_minus_21(theta, phi):
    return 1.03077695553335e-32*(1.0 - cos(theta)**2)**10.5*(8.35764950465071e+39*cos(theta)**16 - 1.37386019254532e+40*cos(theta)**14 + 8.80431531842424e+39*cos(theta)**12 - 2.80717300007729e+39*cos(theta)**10 + 4.71353675386113e+38*cos(theta)**8 - 4.06089320332651e+37*cos(theta)**6 + 1.6114655568756e+36*cos(theta)**4 - 2.26435441247157e+34*cos(theta)**2 + 4.79736104337197e+31)*sin(21*phi)

#@torch.jit.script
def Yl37_m_minus_20(theta, phi):
    return 3.236705294292e-31*(1.0 - cos(theta)**2)**10*(4.91626441450041e+38*cos(theta)**17 - 9.15906795030214e+38*cos(theta)**15 + 6.77255024494173e+38*cos(theta)**13 - 2.55197545461572e+38*cos(theta)**11 + 5.2372630598457e+37*cos(theta)**9 - 5.80127600475216e+36*cos(theta)**7 + 3.2229311137512e+35*cos(theta)**5 - 7.5478480415719e+33*cos(theta)**3 + 4.79736104337197e+31*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl37_m_minus_19(theta, phi):
    return 1.03675667117759e-29*(1.0 - cos(theta)**2)**9.5*(2.73125800805579e+37*cos(theta)**18 - 5.72441746893884e+37*cos(theta)**16 + 4.83753588924409e+37*cos(theta)**14 - 2.12664621217977e+37*cos(theta)**12 + 5.2372630598457e+36*cos(theta)**10 - 7.2515950059402e+35*cos(theta)**8 + 5.371551856252e+34*cos(theta)**6 - 1.88696201039297e+33*cos(theta)**4 + 2.39868052168598e+31*cos(theta)**2 - 4.67579049061595e+28)*sin(19*phi)

#@torch.jit.script
def Yl37_m_minus_18(theta, phi):
    return 3.38179791904549e-28*(1.0 - cos(theta)**2)**9*(1.4375042147662e+36*cos(theta)**19 - 3.36730439349343e+36*cos(theta)**17 + 3.22502392616273e+36*cos(theta)**15 - 1.63588170167675e+36*cos(theta)**13 + 4.76114823622336e+35*cos(theta)**11 - 8.057327784378e+34*cos(theta)**9 + 7.67364550893143e+33*cos(theta)**7 - 3.77392402078595e+32*cos(theta)**5 + 7.99560173895328e+30*cos(theta)**3 - 4.67579049061595e+28*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl37_m_minus_17(theta, phi):
    return 1.12161548142786e-26*(1.0 - cos(theta)**2)**8.5*(7.18752107383102e+34*cos(theta)**20 - 1.87072466305191e+35*cos(theta)**18 + 2.0156399538517e+35*cos(theta)**16 - 1.1684869297691e+35*cos(theta)**14 + 3.96762353018614e+34*cos(theta)**12 - 8.057327784378e+33*cos(theta)**10 + 9.59205688616428e+32*cos(theta)**8 - 6.28987336797658e+31*cos(theta)**6 + 1.99890043473832e+30*cos(theta)**4 - 2.33789524530798e+28*cos(theta)**2 + 4.25071862783268e+25)*sin(17*phi)

#@torch.jit.script
def Yl37_m_minus_16(theta, phi):
    return 3.7770307660841e-25*(1.0 - cos(theta)**2)**8*(3.42262908277667e+33*cos(theta)**21 - 9.84591927922057e+33*cos(theta)**19 + 1.18567056108924e+34*cos(theta)**17 - 7.78991286512736e+33*cos(theta)**15 + 3.05201810014318e+33*cos(theta)**13 - 7.32484344034364e+32*cos(theta)**11 + 1.0657840984627e+32*cos(theta)**9 - 8.98553338282369e+30*cos(theta)**7 + 3.99780086947664e+29*cos(theta)**5 - 7.79298415102659e+27*cos(theta)**3 + 4.25071862783268e+25*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl37_m_minus_15(theta, phi):
    return 1.28973295692034e-23*(1.0 - cos(theta)**2)**7.5*(1.55574049217122e+32*cos(theta)**22 - 4.92295963961028e+32*cos(theta)**20 + 6.58705867271799e+32*cos(theta)**18 - 4.8686955407046e+32*cos(theta)**16 + 2.1800129286737e+32*cos(theta)**14 - 6.10403620028636e+31*cos(theta)**12 + 1.0657840984627e+31*cos(theta)**10 - 1.12319167285296e+30*cos(theta)**8 + 6.66300144912773e+28*cos(theta)**6 - 1.94824603775665e+27*cos(theta)**4 + 2.12535931391634e+25*cos(theta)**2 - 3.64555628459064e+22)*sin(15*phi)

#@torch.jit.script
def Yl37_m_minus_14(theta, phi):
    return 4.4603135268713e-22*(1.0 - cos(theta)**2)**7*(6.76408909639659e+30*cos(theta)**23 - 2.34426649505252e+31*cos(theta)**21 + 3.46687298564105e+31*cos(theta)**19 - 2.86393855335565e+31*cos(theta)**17 + 1.45334195244913e+31*cos(theta)**15 - 4.69541246175874e+30*cos(theta)**13 + 9.68894634966089e+29*cos(theta)**11 - 1.2479907476144e+29*cos(theta)**9 + 9.5185734987539e+27*cos(theta)**7 - 3.89649207551329e+26*cos(theta)**5 + 7.08453104638781e+24*cos(theta)**3 - 3.64555628459064e+22*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl37_m_minus_13(theta, phi):
    return 1.56047241666686e-20*(1.0 - cos(theta)**2)**6.5*(2.81837045683191e+29*cos(theta)**24 - 1.06557567956933e+30*cos(theta)**22 + 1.73343649282052e+30*cos(theta)**20 - 1.59107697408647e+30*cos(theta)**18 + 9.08338720280709e+29*cos(theta)**16 - 3.35386604411339e+29*cos(theta)**14 + 8.07412195805074e+28*cos(theta)**12 - 1.2479907476144e+28*cos(theta)**10 + 1.18982168734424e+27*cos(theta)**8 - 6.49415345918882e+25*cos(theta)**6 + 1.77113276159695e+24*cos(theta)**4 - 1.82277814229532e+22*cos(theta)**2 + 2.97839565734529e+19)*sin(13*phi)

#@torch.jit.script
def Yl37_m_minus_12(theta, phi):
    return 5.51710313839849e-19*(1.0 - cos(theta)**2)**6*(1.12734818273276e+28*cos(theta)**25 - 4.63293773725794e+28*cos(theta)**23 + 8.25445948962154e+28*cos(theta)**21 - 8.37408933729721e+28*cos(theta)**19 + 5.3431689428277e+28*cos(theta)**17 - 2.23591069607559e+28*cos(theta)**15 + 6.21086304465442e+27*cos(theta)**13 - 1.13453704328582e+27*cos(theta)**11 + 1.32202409704915e+26*cos(theta)**9 - 9.27736208455546e+24*cos(theta)**7 + 3.5422655231939e+23*cos(theta)**5 - 6.0759271409844e+21*cos(theta)**3 + 2.97839565734529e+19*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl37_m_minus_11(theta, phi):
    return 1.96922715928385e-17*(1.0 - cos(theta)**2)**5.5*(4.33595454897217e+26*cos(theta)**26 - 1.93039072385747e+27*cos(theta)**24 + 3.75202704073706e+27*cos(theta)**22 - 4.18704466864861e+27*cos(theta)**20 + 2.96842719045983e+27*cos(theta)**18 - 1.39744418504724e+27*cos(theta)**16 + 4.43633074618173e+26*cos(theta)**14 - 9.45447536071516e+25*cos(theta)**12 + 1.32202409704915e+25*cos(theta)**10 - 1.15967026056943e+24*cos(theta)**8 + 5.90377587198984e+22*cos(theta)**6 - 1.5189817852461e+21*cos(theta)**4 + 1.48919782867265e+19*cos(theta)**2 - 2.33783018629929e+16)*sin(11*phi)

#@torch.jit.script
def Yl37_m_minus_10(theta, phi):
    return 7.08921777342186e-16*(1.0 - cos(theta)**2)**5*(1.60590909221192e+25*cos(theta)**27 - 7.7215628954299e+25*cos(theta)**25 + 1.63131610466829e+26*cos(theta)**23 - 1.99383079459457e+26*cos(theta)**21 + 1.56233010024202e+26*cos(theta)**19 - 8.22025991204261e+25*cos(theta)**17 + 2.95755383078782e+25*cos(theta)**15 - 7.27267335439627e+24*cos(theta)**13 + 1.2018400882265e+24*cos(theta)**11 - 1.28852251174381e+23*cos(theta)**9 + 8.43396553141406e+21*cos(theta)**7 - 3.0379635704922e+20*cos(theta)**5 + 4.96399276224215e+18*cos(theta)**3 - 2.33783018629929e+16*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl37_m_minus_9(theta, phi):
    return 2.57173527737449e-14*(1.0 - cos(theta)**2)**4.5*(5.73538961504256e+23*cos(theta)**28 - 2.96983188285765e+24*cos(theta)**26 + 6.79715043611787e+24*cos(theta)**24 - 9.06286724815716e+24*cos(theta)**22 + 7.81165050121009e+24*cos(theta)**20 - 4.5668110622459e+24*cos(theta)**18 + 1.84847114424239e+24*cos(theta)**16 - 5.19476668171163e+23*cos(theta)**14 + 1.00153340685542e+23*cos(theta)**12 - 1.28852251174381e+22*cos(theta)**10 + 1.05424569142676e+21*cos(theta)**8 - 5.063272617487e+19*cos(theta)**6 + 1.24099819056054e+18*cos(theta)**4 - 1.16891509314964e+16*cos(theta)**2 + 17764667069143.5)*sin(9*phi)

#@torch.jit.script
def Yl37_m_minus_8(theta, phi):
    return 9.39299685798656e-13*(1.0 - cos(theta)**2)**4*(1.97772055691123e+22*cos(theta)**29 - 1.09993773439172e+23*cos(theta)**27 + 2.71886017444715e+23*cos(theta)**25 - 3.94037706441615e+23*cos(theta)**23 + 3.7198335720048e+23*cos(theta)**21 - 2.4035847696031e+23*cos(theta)**19 + 1.0873359672014e+23*cos(theta)**17 - 3.46317778780775e+22*cos(theta)**15 + 7.70410312965707e+21*cos(theta)**13 - 1.17138410158529e+21*cos(theta)**11 + 1.17138410158529e+20*cos(theta)**9 - 7.23324659641e+18*cos(theta)**7 + 2.48199638112108e+17*cos(theta)**5 - 3.89638364383215e+15*cos(theta)**3 + 17764667069143.5*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl37_m_minus_7(theta, phi):
    return 3.45120741864491e-11*(1.0 - cos(theta)**2)**3.5*(6.59240185637075e+20*cos(theta)**30 - 3.92834905139901e+21*cos(theta)**28 + 1.04571545171044e+22*cos(theta)**26 - 1.64182377684006e+22*cos(theta)**24 + 1.69083344182036e+22*cos(theta)**22 - 1.20179238480155e+22*cos(theta)**20 + 6.04075537334113e+21*cos(theta)**18 - 2.16448611737984e+21*cos(theta)**16 + 5.50293080689791e+20*cos(theta)**14 - 9.76153417987738e+19*cos(theta)**12 + 1.17138410158529e+19*cos(theta)**10 - 9.0415582455125e+17*cos(theta)**8 + 4.1366606352018e+16*cos(theta)**6 - 974095910958037.0*cos(theta)**4 + 8882333534571.76*cos(theta)**2 - 13159012643.81)*sin(7*phi)

#@torch.jit.script
def Yl37_m_minus_6(theta, phi):
    return 1.27461271489967e-9*(1.0 - cos(theta)**2)**3*(2.12658124399057e+19*cos(theta)**31 - 1.35460312117207e+20*cos(theta)**29 + 3.87302019152015e+20*cos(theta)**27 - 6.56729510736026e+20*cos(theta)**25 + 7.35144974704506e+20*cos(theta)**23 - 5.72282088000739e+20*cos(theta)**21 + 3.17934493333744e+20*cos(theta)**19 - 1.2732271278705e+20*cos(theta)**17 + 3.66862053793194e+19*cos(theta)**15 - 7.50887244605952e+18*cos(theta)**13 + 1.06489463780481e+18*cos(theta)**11 - 1.00461758283472e+17*cos(theta)**9 + 5.90951519314542e+15*cos(theta)**7 - 194819182191607.0*cos(theta)**5 + 2960777844857.25*cos(theta)**3 - 13159012643.81*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl37_m_minus_5(theta, phi):
    return 4.72810881899504e-8*(1.0 - cos(theta)**2)**2.5*(6.64556638747052e+17*cos(theta)**32 - 4.51534373724024e+18*cos(theta)**30 + 1.38322149697148e+19*cos(theta)**28 - 2.5258827336001e+19*cos(theta)**26 + 3.06310406126878e+19*cos(theta)**24 - 2.60128221818518e+19*cos(theta)**22 + 1.58967246666872e+19*cos(theta)**20 - 7.07348404372498e+18*cos(theta)**18 + 2.29288783620746e+18*cos(theta)**16 - 5.36348031861394e+17*cos(theta)**14 + 8.87412198170671e+16*cos(theta)**12 - 1.00461758283472e+16*cos(theta)**10 + 738689399143178.0*cos(theta)**8 - 32469863698601.2*cos(theta)**6 + 740194461214.314*cos(theta)**4 - 6579506321.90501*cos(theta)**2 + 9563235.93300147)*sin(5*phi)

#@torch.jit.script
def Yl37_m_minus_4(theta, phi):
    return 1.76022862219379e-6*(1.0 - cos(theta)**2)**2*(2.01380799620319e+16*cos(theta)**33 - 1.45656249588395e+17*cos(theta)**31 + 4.76972929990167e+17*cos(theta)**29 - 9.35512123555592e+17*cos(theta)**27 + 1.22524162450751e+18*cos(theta)**25 - 1.13099226877616e+18*cos(theta)**23 + 7.56986888889866e+17*cos(theta)**21 - 3.72288633880262e+17*cos(theta)**19 + 1.34875755071027e+17*cos(theta)**17 - 3.57565354574263e+16*cos(theta)**15 + 6.82624767823593e+15*cos(theta)**13 - 913288711667929.0*cos(theta)**11 + 82076599904797.5*cos(theta)**9 - 4638551956943.03*cos(theta)**7 + 148038892242.863*cos(theta)**5 - 2193168773.96834*cos(theta)**3 + 9563235.93300147*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl37_m_minus_3(theta, phi):
    return 6.57204404620968e-5*(1.0 - cos(theta)**2)**1.5*(592296469471526.0*cos(theta)**34 - 4.55175779963734e+15*cos(theta)**32 + 1.58990976663389e+16*cos(theta)**30 - 3.34111472698426e+16*cos(theta)**28 + 4.71246778656735e+16*cos(theta)**26 - 4.71246778656735e+16*cos(theta)**24 + 3.44084949495394e+16*cos(theta)**22 - 1.86144316940131e+16*cos(theta)**20 + 7.49309750394595e+15*cos(theta)**18 - 2.23478346608914e+15*cos(theta)**16 + 487589119873995.0*cos(theta)**14 - 76107392638994.1*cos(theta)**12 + 8207659990479.75*cos(theta)**10 - 579818994617.879*cos(theta)**8 + 24673148707.1438*cos(theta)**6 - 548292193.492084*cos(theta)**4 + 4781617.96650073*cos(theta)**2 - 6860.28402654338)*sin(3*phi)

#@torch.jit.script
def Yl37_m_minus_2(theta, phi):
    return 0.00245903371517041*(1.0 - cos(theta)**2)*(16922756270615.0*cos(theta)**35 - 137932054534465.0*cos(theta)**33 + 512874118268996.0*cos(theta)**31 - 1.1521085265463e+15*cos(theta)**29 + 1.74535843946939e+15*cos(theta)**27 - 1.88498711462694e+15*cos(theta)**25 + 1.49602151954519e+15*cos(theta)**23 - 886401509238719.0*cos(theta)**21 + 394373552839261.0*cos(theta)**19 - 131457850946420.0*cos(theta)**17 + 32505941324933.0*cos(theta)**15 - 5854414818384.16*cos(theta)**13 + 746150908225.432*cos(theta)**11 - 64424332735.3199*cos(theta)**9 + 3524735529.59197*cos(theta)**7 - 109658438.698417*cos(theta)**5 + 1593872.65550024*cos(theta)**3 - 6860.28402654338*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl37_m_minus_1(theta, phi):
    return 0.0921399637754005*(1.0 - cos(theta)**2)**0.5*(470076563072.639*cos(theta)**36 - 4056825133366.61*cos(theta)**34 + 16027316195906.1*cos(theta)**32 - 38403617551543.2*cos(theta)**30 + 62334229981049.6*cos(theta)**28 - 72499504408728.5*cos(theta)**26 + 62334229981049.6*cos(theta)**24 - 40290977692669.1*cos(theta)**22 + 19718677641963.0*cos(theta)**20 - 7303213941467.79*cos(theta)**18 + 2031621332808.31*cos(theta)**16 - 418172487027.44*cos(theta)**14 + 62179242352.1193*cos(theta)**12 - 6442433273.53199*cos(theta)**10 + 440591941.198996*cos(theta)**8 - 18276406.4497361*cos(theta)**6 + 398468.163875061*cos(theta)**4 - 3430.14201327169*cos(theta)**2 + 4.8862421841477)*sin(phi)

#@torch.jit.script
def Yl37_m0(theta, phi):
    return 97508493602.417*cos(theta)**37 - 889598037523.421*cos(theta)**35 + 3727541072721.38*cos(theta)**33 - 9507930852158.88*cos(theta)**31 + 16496969575574.2*cos(theta)**29 - 20608521992871.1*cos(theta)**27 + 19136484707666.0*cos(theta)**25 - 13444837031147.1*cos(theta)**23 + 7206660527288.59*cos(theta)**21 - 2950094952691.24*cos(theta)**19 + 917211339836.73*cos(theta)**17 - 213963537251.793*cos(theta)**15 + 36709430410.8468*cos(theta)**13 - 4495032295.20573*cos(theta)**11 + 375724583.945768*cos(theta)**9 - 20038644.4771076*cos(theta)**7 + 611644.671539622*cos(theta)**5 - 8775.38983557564*cos(theta)**3 + 37.5016659639985*cos(theta)

#@torch.jit.script
def Yl37_m1(theta, phi):
    return 0.0921399637754005*(1.0 - cos(theta)**2)**0.5*(470076563072.639*cos(theta)**36 - 4056825133366.61*cos(theta)**34 + 16027316195906.1*cos(theta)**32 - 38403617551543.2*cos(theta)**30 + 62334229981049.6*cos(theta)**28 - 72499504408728.5*cos(theta)**26 + 62334229981049.6*cos(theta)**24 - 40290977692669.1*cos(theta)**22 + 19718677641963.0*cos(theta)**20 - 7303213941467.79*cos(theta)**18 + 2031621332808.31*cos(theta)**16 - 418172487027.44*cos(theta)**14 + 62179242352.1193*cos(theta)**12 - 6442433273.53199*cos(theta)**10 + 440591941.198996*cos(theta)**8 - 18276406.4497361*cos(theta)**6 + 398468.163875061*cos(theta)**4 - 3430.14201327169*cos(theta)**2 + 4.8862421841477)*cos(phi)

#@torch.jit.script
def Yl37_m2(theta, phi):
    return 0.00245903371517041*(1.0 - cos(theta)**2)*(16922756270615.0*cos(theta)**35 - 137932054534465.0*cos(theta)**33 + 512874118268996.0*cos(theta)**31 - 1.1521085265463e+15*cos(theta)**29 + 1.74535843946939e+15*cos(theta)**27 - 1.88498711462694e+15*cos(theta)**25 + 1.49602151954519e+15*cos(theta)**23 - 886401509238719.0*cos(theta)**21 + 394373552839261.0*cos(theta)**19 - 131457850946420.0*cos(theta)**17 + 32505941324933.0*cos(theta)**15 - 5854414818384.16*cos(theta)**13 + 746150908225.432*cos(theta)**11 - 64424332735.3199*cos(theta)**9 + 3524735529.59197*cos(theta)**7 - 109658438.698417*cos(theta)**5 + 1593872.65550024*cos(theta)**3 - 6860.28402654338*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl37_m3(theta, phi):
    return 6.57204404620968e-5*(1.0 - cos(theta)**2)**1.5*(592296469471526.0*cos(theta)**34 - 4.55175779963734e+15*cos(theta)**32 + 1.58990976663389e+16*cos(theta)**30 - 3.34111472698426e+16*cos(theta)**28 + 4.71246778656735e+16*cos(theta)**26 - 4.71246778656735e+16*cos(theta)**24 + 3.44084949495394e+16*cos(theta)**22 - 1.86144316940131e+16*cos(theta)**20 + 7.49309750394595e+15*cos(theta)**18 - 2.23478346608914e+15*cos(theta)**16 + 487589119873995.0*cos(theta)**14 - 76107392638994.1*cos(theta)**12 + 8207659990479.75*cos(theta)**10 - 579818994617.879*cos(theta)**8 + 24673148707.1438*cos(theta)**6 - 548292193.492084*cos(theta)**4 + 4781617.96650073*cos(theta)**2 - 6860.28402654338)*cos(3*phi)

#@torch.jit.script
def Yl37_m4(theta, phi):
    return 1.76022862219379e-6*(1.0 - cos(theta)**2)**2*(2.01380799620319e+16*cos(theta)**33 - 1.45656249588395e+17*cos(theta)**31 + 4.76972929990167e+17*cos(theta)**29 - 9.35512123555592e+17*cos(theta)**27 + 1.22524162450751e+18*cos(theta)**25 - 1.13099226877616e+18*cos(theta)**23 + 7.56986888889866e+17*cos(theta)**21 - 3.72288633880262e+17*cos(theta)**19 + 1.34875755071027e+17*cos(theta)**17 - 3.57565354574263e+16*cos(theta)**15 + 6.82624767823593e+15*cos(theta)**13 - 913288711667929.0*cos(theta)**11 + 82076599904797.5*cos(theta)**9 - 4638551956943.03*cos(theta)**7 + 148038892242.863*cos(theta)**5 - 2193168773.96834*cos(theta)**3 + 9563235.93300147*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl37_m5(theta, phi):
    return 4.72810881899504e-8*(1.0 - cos(theta)**2)**2.5*(6.64556638747052e+17*cos(theta)**32 - 4.51534373724024e+18*cos(theta)**30 + 1.38322149697148e+19*cos(theta)**28 - 2.5258827336001e+19*cos(theta)**26 + 3.06310406126878e+19*cos(theta)**24 - 2.60128221818518e+19*cos(theta)**22 + 1.58967246666872e+19*cos(theta)**20 - 7.07348404372498e+18*cos(theta)**18 + 2.29288783620746e+18*cos(theta)**16 - 5.36348031861394e+17*cos(theta)**14 + 8.87412198170671e+16*cos(theta)**12 - 1.00461758283472e+16*cos(theta)**10 + 738689399143178.0*cos(theta)**8 - 32469863698601.2*cos(theta)**6 + 740194461214.314*cos(theta)**4 - 6579506321.90501*cos(theta)**2 + 9563235.93300147)*cos(5*phi)

#@torch.jit.script
def Yl37_m6(theta, phi):
    return 1.27461271489967e-9*(1.0 - cos(theta)**2)**3*(2.12658124399057e+19*cos(theta)**31 - 1.35460312117207e+20*cos(theta)**29 + 3.87302019152015e+20*cos(theta)**27 - 6.56729510736026e+20*cos(theta)**25 + 7.35144974704506e+20*cos(theta)**23 - 5.72282088000739e+20*cos(theta)**21 + 3.17934493333744e+20*cos(theta)**19 - 1.2732271278705e+20*cos(theta)**17 + 3.66862053793194e+19*cos(theta)**15 - 7.50887244605952e+18*cos(theta)**13 + 1.06489463780481e+18*cos(theta)**11 - 1.00461758283472e+17*cos(theta)**9 + 5.90951519314542e+15*cos(theta)**7 - 194819182191607.0*cos(theta)**5 + 2960777844857.25*cos(theta)**3 - 13159012643.81*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl37_m7(theta, phi):
    return 3.45120741864491e-11*(1.0 - cos(theta)**2)**3.5*(6.59240185637075e+20*cos(theta)**30 - 3.92834905139901e+21*cos(theta)**28 + 1.04571545171044e+22*cos(theta)**26 - 1.64182377684006e+22*cos(theta)**24 + 1.69083344182036e+22*cos(theta)**22 - 1.20179238480155e+22*cos(theta)**20 + 6.04075537334113e+21*cos(theta)**18 - 2.16448611737984e+21*cos(theta)**16 + 5.50293080689791e+20*cos(theta)**14 - 9.76153417987738e+19*cos(theta)**12 + 1.17138410158529e+19*cos(theta)**10 - 9.0415582455125e+17*cos(theta)**8 + 4.1366606352018e+16*cos(theta)**6 - 974095910958037.0*cos(theta)**4 + 8882333534571.76*cos(theta)**2 - 13159012643.81)*cos(7*phi)

#@torch.jit.script
def Yl37_m8(theta, phi):
    return 9.39299685798656e-13*(1.0 - cos(theta)**2)**4*(1.97772055691123e+22*cos(theta)**29 - 1.09993773439172e+23*cos(theta)**27 + 2.71886017444715e+23*cos(theta)**25 - 3.94037706441615e+23*cos(theta)**23 + 3.7198335720048e+23*cos(theta)**21 - 2.4035847696031e+23*cos(theta)**19 + 1.0873359672014e+23*cos(theta)**17 - 3.46317778780775e+22*cos(theta)**15 + 7.70410312965707e+21*cos(theta)**13 - 1.17138410158529e+21*cos(theta)**11 + 1.17138410158529e+20*cos(theta)**9 - 7.23324659641e+18*cos(theta)**7 + 2.48199638112108e+17*cos(theta)**5 - 3.89638364383215e+15*cos(theta)**3 + 17764667069143.5*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl37_m9(theta, phi):
    return 2.57173527737449e-14*(1.0 - cos(theta)**2)**4.5*(5.73538961504256e+23*cos(theta)**28 - 2.96983188285765e+24*cos(theta)**26 + 6.79715043611787e+24*cos(theta)**24 - 9.06286724815716e+24*cos(theta)**22 + 7.81165050121009e+24*cos(theta)**20 - 4.5668110622459e+24*cos(theta)**18 + 1.84847114424239e+24*cos(theta)**16 - 5.19476668171163e+23*cos(theta)**14 + 1.00153340685542e+23*cos(theta)**12 - 1.28852251174381e+22*cos(theta)**10 + 1.05424569142676e+21*cos(theta)**8 - 5.063272617487e+19*cos(theta)**6 + 1.24099819056054e+18*cos(theta)**4 - 1.16891509314964e+16*cos(theta)**2 + 17764667069143.5)*cos(9*phi)

#@torch.jit.script
def Yl37_m10(theta, phi):
    return 7.08921777342186e-16*(1.0 - cos(theta)**2)**5*(1.60590909221192e+25*cos(theta)**27 - 7.7215628954299e+25*cos(theta)**25 + 1.63131610466829e+26*cos(theta)**23 - 1.99383079459457e+26*cos(theta)**21 + 1.56233010024202e+26*cos(theta)**19 - 8.22025991204261e+25*cos(theta)**17 + 2.95755383078782e+25*cos(theta)**15 - 7.27267335439627e+24*cos(theta)**13 + 1.2018400882265e+24*cos(theta)**11 - 1.28852251174381e+23*cos(theta)**9 + 8.43396553141406e+21*cos(theta)**7 - 3.0379635704922e+20*cos(theta)**5 + 4.96399276224215e+18*cos(theta)**3 - 2.33783018629929e+16*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl37_m11(theta, phi):
    return 1.96922715928385e-17*(1.0 - cos(theta)**2)**5.5*(4.33595454897217e+26*cos(theta)**26 - 1.93039072385747e+27*cos(theta)**24 + 3.75202704073706e+27*cos(theta)**22 - 4.18704466864861e+27*cos(theta)**20 + 2.96842719045983e+27*cos(theta)**18 - 1.39744418504724e+27*cos(theta)**16 + 4.43633074618173e+26*cos(theta)**14 - 9.45447536071516e+25*cos(theta)**12 + 1.32202409704915e+25*cos(theta)**10 - 1.15967026056943e+24*cos(theta)**8 + 5.90377587198984e+22*cos(theta)**6 - 1.5189817852461e+21*cos(theta)**4 + 1.48919782867265e+19*cos(theta)**2 - 2.33783018629929e+16)*cos(11*phi)

#@torch.jit.script
def Yl37_m12(theta, phi):
    return 5.51710313839849e-19*(1.0 - cos(theta)**2)**6*(1.12734818273276e+28*cos(theta)**25 - 4.63293773725794e+28*cos(theta)**23 + 8.25445948962154e+28*cos(theta)**21 - 8.37408933729721e+28*cos(theta)**19 + 5.3431689428277e+28*cos(theta)**17 - 2.23591069607559e+28*cos(theta)**15 + 6.21086304465442e+27*cos(theta)**13 - 1.13453704328582e+27*cos(theta)**11 + 1.32202409704915e+26*cos(theta)**9 - 9.27736208455546e+24*cos(theta)**7 + 3.5422655231939e+23*cos(theta)**5 - 6.0759271409844e+21*cos(theta)**3 + 2.97839565734529e+19*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl37_m13(theta, phi):
    return 1.56047241666686e-20*(1.0 - cos(theta)**2)**6.5*(2.81837045683191e+29*cos(theta)**24 - 1.06557567956933e+30*cos(theta)**22 + 1.73343649282052e+30*cos(theta)**20 - 1.59107697408647e+30*cos(theta)**18 + 9.08338720280709e+29*cos(theta)**16 - 3.35386604411339e+29*cos(theta)**14 + 8.07412195805074e+28*cos(theta)**12 - 1.2479907476144e+28*cos(theta)**10 + 1.18982168734424e+27*cos(theta)**8 - 6.49415345918882e+25*cos(theta)**6 + 1.77113276159695e+24*cos(theta)**4 - 1.82277814229532e+22*cos(theta)**2 + 2.97839565734529e+19)*cos(13*phi)

#@torch.jit.script
def Yl37_m14(theta, phi):
    return 4.4603135268713e-22*(1.0 - cos(theta)**2)**7*(6.76408909639659e+30*cos(theta)**23 - 2.34426649505252e+31*cos(theta)**21 + 3.46687298564105e+31*cos(theta)**19 - 2.86393855335565e+31*cos(theta)**17 + 1.45334195244913e+31*cos(theta)**15 - 4.69541246175874e+30*cos(theta)**13 + 9.68894634966089e+29*cos(theta)**11 - 1.2479907476144e+29*cos(theta)**9 + 9.5185734987539e+27*cos(theta)**7 - 3.89649207551329e+26*cos(theta)**5 + 7.08453104638781e+24*cos(theta)**3 - 3.64555628459064e+22*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl37_m15(theta, phi):
    return 1.28973295692034e-23*(1.0 - cos(theta)**2)**7.5*(1.55574049217122e+32*cos(theta)**22 - 4.92295963961028e+32*cos(theta)**20 + 6.58705867271799e+32*cos(theta)**18 - 4.8686955407046e+32*cos(theta)**16 + 2.1800129286737e+32*cos(theta)**14 - 6.10403620028636e+31*cos(theta)**12 + 1.0657840984627e+31*cos(theta)**10 - 1.12319167285296e+30*cos(theta)**8 + 6.66300144912773e+28*cos(theta)**6 - 1.94824603775665e+27*cos(theta)**4 + 2.12535931391634e+25*cos(theta)**2 - 3.64555628459064e+22)*cos(15*phi)

#@torch.jit.script
def Yl37_m16(theta, phi):
    return 3.7770307660841e-25*(1.0 - cos(theta)**2)**8*(3.42262908277667e+33*cos(theta)**21 - 9.84591927922057e+33*cos(theta)**19 + 1.18567056108924e+34*cos(theta)**17 - 7.78991286512736e+33*cos(theta)**15 + 3.05201810014318e+33*cos(theta)**13 - 7.32484344034364e+32*cos(theta)**11 + 1.0657840984627e+32*cos(theta)**9 - 8.98553338282369e+30*cos(theta)**7 + 3.99780086947664e+29*cos(theta)**5 - 7.79298415102659e+27*cos(theta)**3 + 4.25071862783268e+25*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl37_m17(theta, phi):
    return 1.12161548142786e-26*(1.0 - cos(theta)**2)**8.5*(7.18752107383102e+34*cos(theta)**20 - 1.87072466305191e+35*cos(theta)**18 + 2.0156399538517e+35*cos(theta)**16 - 1.1684869297691e+35*cos(theta)**14 + 3.96762353018614e+34*cos(theta)**12 - 8.057327784378e+33*cos(theta)**10 + 9.59205688616428e+32*cos(theta)**8 - 6.28987336797658e+31*cos(theta)**6 + 1.99890043473832e+30*cos(theta)**4 - 2.33789524530798e+28*cos(theta)**2 + 4.25071862783268e+25)*cos(17*phi)

#@torch.jit.script
def Yl37_m18(theta, phi):
    return 3.38179791904549e-28*(1.0 - cos(theta)**2)**9*(1.4375042147662e+36*cos(theta)**19 - 3.36730439349343e+36*cos(theta)**17 + 3.22502392616273e+36*cos(theta)**15 - 1.63588170167675e+36*cos(theta)**13 + 4.76114823622336e+35*cos(theta)**11 - 8.057327784378e+34*cos(theta)**9 + 7.67364550893143e+33*cos(theta)**7 - 3.77392402078595e+32*cos(theta)**5 + 7.99560173895328e+30*cos(theta)**3 - 4.67579049061595e+28*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl37_m19(theta, phi):
    return 1.03675667117759e-29*(1.0 - cos(theta)**2)**9.5*(2.73125800805579e+37*cos(theta)**18 - 5.72441746893884e+37*cos(theta)**16 + 4.83753588924409e+37*cos(theta)**14 - 2.12664621217977e+37*cos(theta)**12 + 5.2372630598457e+36*cos(theta)**10 - 7.2515950059402e+35*cos(theta)**8 + 5.371551856252e+34*cos(theta)**6 - 1.88696201039297e+33*cos(theta)**4 + 2.39868052168598e+31*cos(theta)**2 - 4.67579049061595e+28)*cos(19*phi)

#@torch.jit.script
def Yl37_m20(theta, phi):
    return 3.236705294292e-31*(1.0 - cos(theta)**2)**10*(4.91626441450041e+38*cos(theta)**17 - 9.15906795030214e+38*cos(theta)**15 + 6.77255024494173e+38*cos(theta)**13 - 2.55197545461572e+38*cos(theta)**11 + 5.2372630598457e+37*cos(theta)**9 - 5.80127600475216e+36*cos(theta)**7 + 3.2229311137512e+35*cos(theta)**5 - 7.5478480415719e+33*cos(theta)**3 + 4.79736104337197e+31*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl37_m21(theta, phi):
    return 1.03077695553335e-32*(1.0 - cos(theta)**2)**10.5*(8.35764950465071e+39*cos(theta)**16 - 1.37386019254532e+40*cos(theta)**14 + 8.80431531842424e+39*cos(theta)**12 - 2.80717300007729e+39*cos(theta)**10 + 4.71353675386113e+38*cos(theta)**8 - 4.06089320332651e+37*cos(theta)**6 + 1.6114655568756e+36*cos(theta)**4 - 2.26435441247157e+34*cos(theta)**2 + 4.79736104337197e+31)*cos(21*phi)

#@torch.jit.script
def Yl37_m22(theta, phi):
    return 3.3548932326254e-34*(1.0 - cos(theta)**2)**11*(1.33722392074411e+41*cos(theta)**15 - 1.92340426956345e+41*cos(theta)**13 + 1.05651783821091e+41*cos(theta)**11 - 2.80717300007729e+40*cos(theta)**9 + 3.7708294030889e+39*cos(theta)**7 - 2.43653592199591e+38*cos(theta)**5 + 6.4458622275024e+36*cos(theta)**3 - 4.52870882494314e+34*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl37_m23(theta, phi):
    return 1.11829774420847e-35*(1.0 - cos(theta)**2)**11.5*(2.00583588111617e+42*cos(theta)**14 - 2.50042555043248e+42*cos(theta)**12 + 1.162169622032e+42*cos(theta)**10 - 2.52645570006957e+41*cos(theta)**8 + 2.63958058216223e+40*cos(theta)**6 - 1.21826796099795e+39*cos(theta)**4 + 1.93375866825072e+37*cos(theta)**2 - 4.52870882494314e+34)*cos(23*phi)

#@torch.jit.script
def Yl37_m24(theta, phi):
    return 3.82673610124151e-37*(1.0 - cos(theta)**2)**12*(2.80817023356264e+43*cos(theta)**13 - 3.00051066051898e+43*cos(theta)**11 + 1.162169622032e+43*cos(theta)**9 - 2.02116456005565e+42*cos(theta)**7 + 1.58374834929734e+41*cos(theta)**5 - 4.87307184399181e+39*cos(theta)**3 + 3.86751733650144e+37*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl37_m25(theta, phi):
    return 1.34791030198661e-38*(1.0 - cos(theta)**2)**12.5*(3.65062130363143e+44*cos(theta)**12 - 3.30056172657088e+44*cos(theta)**10 + 1.0459526598288e+44*cos(theta)**8 - 1.41481519203896e+43*cos(theta)**6 + 7.9187417464867e+41*cos(theta)**4 - 1.46192155319754e+40*cos(theta)**2 + 3.86751733650144e+37)*cos(25*phi)

#@torch.jit.script
def Yl37_m26(theta, phi):
    return 4.90230237211461e-40*(1.0 - cos(theta)**2)**13*(4.38074556435771e+45*cos(theta)**11 - 3.30056172657088e+45*cos(theta)**9 + 8.3676212786304e+44*cos(theta)**7 - 8.48889115223374e+43*cos(theta)**5 + 3.16749669859468e+42*cos(theta)**3 - 2.92384310639509e+40*cos(theta))*cos(26*phi)

#@torch.jit.script
def Yl37_m27(theta, phi):
    return 1.84762472467879e-41*(1.0 - cos(theta)**2)**13.5*(4.81882012079349e+46*cos(theta)**10 - 2.97050555391379e+46*cos(theta)**8 + 5.85733489504128e+45*cos(theta)**6 - 4.24444557611687e+44*cos(theta)**4 + 9.50249009578404e+42*cos(theta)**2 - 2.92384310639509e+40)*cos(27*phi)

#@torch.jit.script
def Yl37_m28(theta, phi):
    return 7.24698040379513e-43*(1.0 - cos(theta)**2)**14*(4.81882012079349e+47*cos(theta)**9 - 2.37640444313103e+47*cos(theta)**7 + 3.51440093702477e+46*cos(theta)**5 - 1.69777823044675e+45*cos(theta)**3 + 1.90049801915681e+43*cos(theta))*cos(28*phi)

#@torch.jit.script
def Yl37_m29(theta, phi):
    return 2.9734720766705e-44*(1.0 - cos(theta)**2)**14.5*(4.33693810871414e+48*cos(theta)**8 - 1.66348311019172e+48*cos(theta)**6 + 1.75720046851238e+47*cos(theta)**4 - 5.09333469134024e+45*cos(theta)**2 + 1.90049801915681e+43)*cos(29*phi)

#@torch.jit.script
def Yl37_m30(theta, phi):
    return 1.28434432069174e-45*(1.0 - cos(theta)**2)**15*(3.46955048697131e+49*cos(theta)**7 - 9.98089866115034e+48*cos(theta)**5 + 7.02880187404954e+47*cos(theta)**3 - 1.01866693826805e+46*cos(theta))*cos(30*phi)

#@torch.jit.script
def Yl37_m31(theta, phi):
    return 5.88678254222418e-47*(1.0 - cos(theta)**2)**15.5*(2.42868534087992e+50*cos(theta)**6 - 4.99044933057517e+49*cos(theta)**4 + 2.10864056221486e+48*cos(theta)**2 - 1.01866693826805e+46)*cos(31*phi)

#@torch.jit.script
def Yl37_m32(theta, phi):
    return 2.89319577828011e-48*(1.0 - cos(theta)**2)**16*(1.45721120452795e+51*cos(theta)**5 - 1.99617973223007e+50*cos(theta)**3 + 4.21728112442972e+48*cos(theta))*cos(32*phi)

#@torch.jit.script
def Yl37_m33(theta, phi):
    return 1.54647819359785e-49*(1.0 - cos(theta)**2)**16.5*(7.28605602263975e+51*cos(theta)**4 - 5.98853919669021e+50*cos(theta)**2 + 4.21728112442972e+48)*cos(33*phi)

#@torch.jit.script
def Yl37_m34(theta, phi):
    return 9.17665977479345e-51*(1.0 - cos(theta)**2)**17*(2.9144224090559e+52*cos(theta)**3 - 1.19770783933804e+51*cos(theta))*cos(34*phi)

#@torch.jit.script
def Yl37_m35(theta, phi):
    return 6.24392610871321e-52*(1.0 - cos(theta)**2)**17.5*(8.7432672271677e+52*cos(theta)**2 - 1.19770783933804e+51)*cos(35*phi)

#@torch.jit.script
def Yl37_m36(theta, phi):
    return 9.03618419303727*(1.0 - cos(theta)**2)**18*cos(36*phi)*cos(theta)

#@torch.jit.script
def Yl37_m37(theta, phi):
    return 1.05043507569481*(1.0 - cos(theta)**2)**18.5*cos(37*phi)

#@torch.jit.script
def Yl38_m_minus_38(theta, phi):
    return 1.0573232483571*(1.0 - cos(theta)**2)**19*sin(38*phi)

#@torch.jit.script
def Yl38_m_minus_37(theta, phi):
    return 9.21753038048947*(1.0 - cos(theta)**2)**18.5*sin(37*phi)*cos(theta)

#@torch.jit.script
def Yl38_m_minus_36(theta, phi):
    return 8.60786001928606e-54*(1.0 - cos(theta)**2)**18*(6.55745042037577e+54*cos(theta)**2 - 8.7432672271677e+52)*sin(36*phi)

#@torch.jit.script
def Yl38_m_minus_35(theta, phi):
    return 1.28254225711204e-52*(1.0 - cos(theta)**2)**17.5*(2.18581680679192e+54*cos(theta)**3 - 8.7432672271677e+52*cos(theta))*sin(35*phi)

#@torch.jit.script
def Yl38_m_minus_34(theta, phi):
    return 2.19160916965865e-51*(1.0 - cos(theta)**2)**17*(5.46454201697981e+53*cos(theta)**4 - 4.37163361358385e+52*cos(theta)**2 + 2.9942695983451e+50)*sin(34*phi)

#@torch.jit.script
def Yl38_m_minus_33(theta, phi):
    return 4.15828603021903e-50*(1.0 - cos(theta)**2)**16.5*(1.09290840339596e+53*cos(theta)**5 - 1.45721120452795e+52*cos(theta)**3 + 2.9942695983451e+50*cos(theta))*sin(33*phi)

#@torch.jit.script
def Yl38_m_minus_32(theta, phi):
    return 8.58260566150099e-49*(1.0 - cos(theta)**2)**16*(1.82151400565994e+52*cos(theta)**6 - 3.64302801131987e+51*cos(theta)**4 + 1.49713479917255e+50*cos(theta)**2 - 7.02880187404954e+47)*sin(32*phi)

#@torch.jit.script
def Yl38_m_minus_31(theta, phi):
    return 1.89984075045795e-47*(1.0 - cos(theta)**2)**15.5*(2.60216286522848e+51*cos(theta)**7 - 7.28605602263975e+50*cos(theta)**5 + 4.99044933057517e+49*cos(theta)**3 - 7.02880187404954e+47*cos(theta))*sin(31*phi)

#@torch.jit.script
def Yl38_m_minus_30(theta, phi):
    return 4.46361509559185e-46*(1.0 - cos(theta)**2)**15*(3.2527035815356e+50*cos(theta)**8 - 1.21434267043996e+50*cos(theta)**6 + 1.24761233264379e+49*cos(theta)**4 - 3.51440093702477e+47*cos(theta)**2 + 1.27333367283506e+45)*sin(30*phi)

#@torch.jit.script
def Yl38_m_minus_29(theta, phi):
    return 1.1042373906736e-44*(1.0 - cos(theta)**2)**14.5*(3.61411509059511e+49*cos(theta)**9 - 1.73477524348565e+49*cos(theta)**7 + 2.49522466528759e+48*cos(theta)**5 - 1.17146697900826e+47*cos(theta)**3 + 1.27333367283506e+45*cos(theta))*sin(29*phi)

#@torch.jit.script
def Yl38_m_minus_28(theta, phi):
    return 2.85824761702743e-43*(1.0 - cos(theta)**2)**14*(3.61411509059511e+48*cos(theta)**10 - 2.16846905435707e+48*cos(theta)**8 + 4.15870777547931e+47*cos(theta)**6 - 2.92866744752064e+46*cos(theta)**4 + 6.3666683641753e+44*cos(theta)**2 - 1.90049801915681e+42)*sin(28*phi)

#@torch.jit.script
def Yl38_m_minus_27(theta, phi):
    return 7.70137304226747e-42*(1.0 - cos(theta)**2)**13.5*(3.28555917326829e+47*cos(theta)**11 - 2.40941006039674e+47*cos(theta)**9 + 5.94101110782758e+46*cos(theta)**7 - 5.85733489504128e+45*cos(theta)**5 + 2.12222278805844e+44*cos(theta)**3 - 1.90049801915681e+42*cos(theta))*sin(27*phi)

#@torch.jit.script
def Yl38_m_minus_26(theta, phi):
    return 2.15087643657668e-40*(1.0 - cos(theta)**2)**13*(2.73796597772357e+46*cos(theta)**12 - 2.40941006039674e+46*cos(theta)**10 + 7.42626388478448e+45*cos(theta)**8 - 9.7622248250688e+44*cos(theta)**6 + 5.30555697014609e+43*cos(theta)**4 - 9.50249009578404e+41*cos(theta)**2 + 2.43653592199591e+39)*sin(26*phi)

#@torch.jit.script
def Yl38_m_minus_25(theta, phi):
    return 6.20407622341159e-39*(1.0 - cos(theta)**2)**12.5*(2.10612767517198e+45*cos(theta)**13 - 2.19037278217886e+45*cos(theta)**11 + 8.2514043164272e+44*cos(theta)**9 - 1.3946035464384e+44*cos(theta)**7 + 1.06111139402922e+43*cos(theta)**5 - 3.16749669859468e+41*cos(theta)**3 + 2.43653592199591e+39*cos(theta))*sin(25*phi)

#@torch.jit.script
def Yl38_m_minus_24(theta, phi):
    return 1.84251663480048e-37*(1.0 - cos(theta)**2)**12*(1.50437691083713e+44*cos(theta)**14 - 1.82531065181571e+44*cos(theta)**12 + 8.2514043164272e+43*cos(theta)**10 - 1.743254433048e+43*cos(theta)**8 + 1.7685189900487e+42*cos(theta)**6 - 7.9187417464867e+40*cos(theta)**4 + 1.21826796099795e+39*cos(theta)**2 - 2.76251238321531e+36)*sin(24*phi)

#@torch.jit.script
def Yl38_m_minus_23(theta, phi):
    return 5.61892055563194e-36*(1.0 - cos(theta)**2)**11.5*(1.00291794055808e+43*cos(theta)**15 - 1.40408511678132e+43*cos(theta)**13 + 7.50127665129745e+42*cos(theta)**11 - 1.93694937005333e+42*cos(theta)**9 + 2.52645570006957e+41*cos(theta)**7 - 1.58374834929734e+40*cos(theta)**5 + 4.06089320332651e+38*cos(theta)**3 - 2.76251238321531e+36*cos(theta))*sin(23*phi)

#@torch.jit.script
def Yl38_m_minus_22(theta, phi):
    return 1.75540689794278e-34*(1.0 - cos(theta)**2)**11*(6.26823712848803e+41*cos(theta)**16 - 1.00291794055808e+42*cos(theta)**14 + 6.25106387608121e+41*cos(theta)**12 - 1.93694937005333e+41*cos(theta)**10 + 3.15806962508696e+40*cos(theta)**8 - 2.63958058216223e+39*cos(theta)**6 + 1.01522330083163e+38*cos(theta)**4 - 1.38125619160766e+36*cos(theta)**2 + 2.83044301558946e+33)*sin(22*phi)

#@torch.jit.script
def Yl38_m_minus_21(theta, phi):
    return 5.60632004517403e-33*(1.0 - cos(theta)**2)**10.5*(3.68719831087531e+40*cos(theta)**17 - 6.68611960372056e+40*cos(theta)**15 + 4.80851067390862e+40*cos(theta)**13 - 1.76086306368485e+40*cos(theta)**11 + 3.50896625009662e+39*cos(theta)**9 - 3.7708294030889e+38*cos(theta)**7 + 2.03044660166326e+37*cos(theta)**5 - 4.60418730535886e+35*cos(theta)**3 + 2.83044301558946e+33*cos(theta))*sin(21*phi)

#@torch.jit.script
def Yl38_m_minus_20(theta, phi):
    return 1.82700672042423e-31*(1.0 - cos(theta)**2)**10*(2.04844350604184e+39*cos(theta)**18 - 4.17882475232535e+39*cos(theta)**16 + 3.4346504813633e+39*cos(theta)**14 - 1.46738588640404e+39*cos(theta)**12 + 3.50896625009662e+38*cos(theta)**10 - 4.71353675386113e+37*cos(theta)**8 + 3.38407766943876e+36*cos(theta)**6 - 1.15104682633971e+35*cos(theta)**4 + 1.41522150779473e+33*cos(theta)**2 - 2.66520057965109e+30)*sin(20*phi)

#@torch.jit.script
def Yl38_m_minus_19(theta, phi):
    return 6.06500191198304e-30*(1.0 - cos(theta)**2)**9.5*(1.07812816107465e+38*cos(theta)**19 - 2.45813220725021e+38*cos(theta)**17 + 2.28976698757554e+38*cos(theta)**15 - 1.12875837415695e+38*cos(theta)**13 + 3.18996931826965e+37*cos(theta)**11 - 5.2372630598457e+36*cos(theta)**9 + 4.8343966706268e+35*cos(theta)**7 - 2.30209365267943e+34*cos(theta)**5 + 4.71740502598244e+32*cos(theta)**3 - 2.66520057965109e+30*cos(theta))*sin(19*phi)

#@torch.jit.script
def Yl38_m_minus_18(theta, phi):
    return 2.04778033341685e-28*(1.0 - cos(theta)**2)**9*(5.39064080537326e+36*cos(theta)**20 - 1.36562900402789e+37*cos(theta)**18 + 1.43110436723471e+37*cos(theta)**16 - 8.06255981540682e+36*cos(theta)**14 + 2.65830776522471e+36*cos(theta)**12 - 5.2372630598457e+35*cos(theta)**10 + 6.0429958382835e+34*cos(theta)**8 - 3.83682275446571e+33*cos(theta)**6 + 1.17935125649561e+32*cos(theta)**4 - 1.33260028982555e+30*cos(theta)**2 + 2.33789524530798e+27)*sin(18*phi)

#@torch.jit.script
def Yl38_m_minus_17(theta, phi):
    return 7.02242369104875e-27*(1.0 - cos(theta)**2)**8.5*(2.56697181208251e+35*cos(theta)**21 - 7.18752107383102e+35*cos(theta)**19 + 8.41826098373359e+35*cos(theta)**17 - 5.37503987693788e+35*cos(theta)**15 + 2.04485212709593e+35*cos(theta)**13 - 4.76114823622336e+34*cos(theta)**11 + 6.714439820315e+33*cos(theta)**9 - 5.48117536352245e+32*cos(theta)**7 + 2.35870251299122e+31*cos(theta)**5 - 4.44200096608516e+29*cos(theta)**3 + 2.33789524530798e+27*cos(theta))*sin(17*phi)

#@torch.jit.script
def Yl38_m_minus_16(theta, phi):
    return 2.44275389142847e-25*(1.0 - cos(theta)**2)**8*(1.16680536912841e+34*cos(theta)**22 - 3.59376053691551e+34*cos(theta)**20 + 4.67681165762977e+34*cos(theta)**18 - 3.35939992308617e+34*cos(theta)**16 + 1.46060866221138e+34*cos(theta)**14 - 3.96762353018614e+33*cos(theta)**12 + 6.714439820315e+32*cos(theta)**10 - 6.85146920440306e+31*cos(theta)**8 + 3.93117085498536e+30*cos(theta)**6 - 1.11050024152129e+29*cos(theta)**4 + 1.16894762265399e+27*cos(theta)**2 - 1.93214483083304e+24)*sin(16*phi)

#@torch.jit.script
def Yl38_m_minus_15(theta, phi):
    return 8.60875824089541e-24*(1.0 - cos(theta)**2)**7.5*(5.07306682229744e+32*cos(theta)**23 - 1.71131454138834e+33*cos(theta)**21 + 2.46147981980514e+33*cos(theta)**19 - 1.9761176018154e+33*cos(theta)**17 + 9.7373910814092e+32*cos(theta)**15 - 3.05201810014318e+32*cos(theta)**13 + 6.10403620028636e+31*cos(theta)**11 - 7.61274356044785e+30*cos(theta)**9 + 5.6159583642648e+29*cos(theta)**7 - 2.22100048304258e+28*cos(theta)**5 + 3.89649207551329e+26*cos(theta)**3 - 1.93214483083304e+24*cos(theta))*sin(15*phi)

#@torch.jit.script
def Yl38_m_minus_14(theta, phi):
    return 3.0703230101837e-22*(1.0 - cos(theta)**2)**7*(2.11377784262393e+31*cos(theta)**24 - 7.77870246085608e+31*cos(theta)**22 + 1.23073990990257e+32*cos(theta)**20 - 1.09784311211966e+32*cos(theta)**18 + 6.08586942588075e+31*cos(theta)**16 - 2.1800129286737e+31*cos(theta)**14 + 5.08669683357197e+30*cos(theta)**12 - 7.61274356044784e+29*cos(theta)**10 + 7.019947955331e+28*cos(theta)**8 - 3.70166747173763e+27*cos(theta)**6 + 9.74123018878324e+25*cos(theta)**4 - 9.66072415416519e+23*cos(theta)**2 + 1.5189817852461e+21)*sin(14*phi)

#@torch.jit.script
def Yl38_m_minus_13(theta, phi):
    return 1.10702070454543e-20*(1.0 - cos(theta)**2)**6.5*(8.45511137049574e+29*cos(theta)**25 - 3.38204454819829e+30*cos(theta)**23 + 5.86066623763129e+30*cos(theta)**21 - 5.77812164273508e+30*cos(theta)**19 + 3.57992319169456e+30*cos(theta)**17 - 1.45334195244913e+30*cos(theta)**15 + 3.91284371813228e+29*cos(theta)**13 - 6.9206759640435e+28*cos(theta)**11 + 7.79994217259001e+27*cos(theta)**9 - 5.28809638819661e+26*cos(theta)**7 + 1.94824603775665e+25*cos(theta)**5 - 3.22024138472173e+23*cos(theta)**3 + 1.5189817852461e+21*cos(theta))*sin(13*phi)

#@torch.jit.script
def Yl38_m_minus_12(theta, phi):
    return 4.03113651248321e-19*(1.0 - cos(theta)**2)**6*(3.25196591172913e+28*cos(theta)**26 - 1.40918522841596e+29*cos(theta)**24 + 2.66393919892331e+29*cos(theta)**22 - 2.88906082136754e+29*cos(theta)**20 + 1.98884621760809e+29*cos(theta)**18 - 9.08338720280709e+28*cos(theta)**16 + 2.79488837009449e+28*cos(theta)**14 - 5.76722997003625e+27*cos(theta)**12 + 7.79994217259e+26*cos(theta)**10 - 6.61012048524577e+25*cos(theta)**8 + 3.24707672959441e+24*cos(theta)**6 - 8.05060346180433e+22*cos(theta)**4 + 7.5949089262305e+20*cos(theta)**2 - 1.14553679128665e+18)*sin(12*phi)

#@torch.jit.script
def Yl38_m_minus_11(theta, phi):
    return 1.48113413086296e-17*(1.0 - cos(theta)**2)**5.5*(1.20443181915894e+27*cos(theta)**27 - 5.63674091366382e+27*cos(theta)**25 + 1.15823443431448e+28*cos(theta)**23 - 1.37574324827026e+28*cos(theta)**21 + 1.04676116716215e+28*cos(theta)**19 - 5.3431689428277e+27*cos(theta)**17 + 1.86325891339633e+27*cos(theta)**15 - 4.43633074618173e+26*cos(theta)**13 + 7.09085652053637e+25*cos(theta)**11 - 7.34457831693974e+24*cos(theta)**9 + 4.63868104227773e+23*cos(theta)**7 - 1.61012069236087e+22*cos(theta)**5 + 2.5316363087435e+20*cos(theta)**3 - 1.14553679128665e+18*cos(theta))*sin(11*phi)

#@torch.jit.script
def Yl38_m_minus_10(theta, phi):
    return 5.48619759603045e-16*(1.0 - cos(theta)**2)**5*(4.30154221128192e+25*cos(theta)**28 - 2.16797727448609e+26*cos(theta)**26 + 4.82597680964369e+26*cos(theta)**24 - 6.25337840122844e+26*cos(theta)**22 + 5.23380583581076e+26*cos(theta)**20 - 2.96842719045983e+26*cos(theta)**18 + 1.1645368208727e+26*cos(theta)**16 - 3.16880767584409e+25*cos(theta)**14 + 5.90904710044697e+24*cos(theta)**12 - 7.34457831693974e+23*cos(theta)**10 + 5.79835130284716e+22*cos(theta)**8 - 2.68353448726811e+21*cos(theta)**6 + 6.32909077185875e+19*cos(theta)**4 - 5.72768395643326e+17*cos(theta)**2 + 834939352249746.0)*sin(10*phi)

#@torch.jit.script
def Yl38_m_minus_9(theta, phi):
    return 2.04687378153282e-14*(1.0 - cos(theta)**2)**4.5*(1.48329041768342e+24*cos(theta)**29 - 8.02954546105958e+24*cos(theta)**27 + 1.93039072385747e+25*cos(theta)**25 - 2.71886017444715e+25*cos(theta)**23 + 2.49228849324322e+25*cos(theta)**21 - 1.56233010024202e+25*cos(theta)**19 + 6.85021659336884e+24*cos(theta)**17 - 2.11253845056273e+24*cos(theta)**15 + 4.54542084649767e+23*cos(theta)**13 - 6.67688937903613e+22*cos(theta)**11 + 6.44261255871907e+21*cos(theta)**9 - 3.8336206960973e+20*cos(theta)**7 + 1.26581815437175e+19*cos(theta)**5 - 1.90922798547775e+17*cos(theta)**3 + 834939352249746.0*cos(theta))*sin(9*phi)

#@torch.jit.script
def Yl38_m_minus_8(theta, phi):
    return 7.68600423582523e-13*(1.0 - cos(theta)**2)**4*(4.94430139227807e+22*cos(theta)**30 - 2.86769480752128e+23*cos(theta)**28 + 7.42457970714413e+23*cos(theta)**26 - 1.13285840601964e+24*cos(theta)**24 + 1.13285840601964e+24*cos(theta)**22 - 7.81165050121009e+23*cos(theta)**20 + 3.80567588520491e+23*cos(theta)**18 - 1.3203365316017e+23*cos(theta)**16 + 3.24672917606977e+22*cos(theta)**14 - 5.56407448253011e+21*cos(theta)**12 + 6.44261255871907e+20*cos(theta)**10 - 4.79202587012162e+19*cos(theta)**8 + 2.10969692395292e+18*cos(theta)**6 - 4.77306996369438e+16*cos(theta)**4 + 417469676124873.0*cos(theta)**2 - 592155568971.451)*sin(8*phi)

#@torch.jit.script
def Yl38_m_minus_7(theta, phi):
    return 2.90242083005401e-11*(1.0 - cos(theta)**2)**3.5*(1.59493593299292e+21*cos(theta)**31 - 9.88860278455613e+21*cos(theta)**29 + 2.74984433597931e+22*cos(theta)**27 - 4.53143362407858e+22*cos(theta)**25 + 4.92547133052019e+22*cos(theta)**23 - 3.7198335720048e+22*cos(theta)**21 + 2.00298730800259e+22*cos(theta)**19 - 7.76668548001003e+21*cos(theta)**17 + 2.16448611737984e+21*cos(theta)**15 - 4.28005729425393e+20*cos(theta)**13 + 5.85692050792643e+19*cos(theta)**11 - 5.32447318902403e+18*cos(theta)**9 + 3.01385274850417e+17*cos(theta)**7 - 9.54613992738876e+15*cos(theta)**5 + 139156558708291.0*cos(theta)**3 - 592155568971.451*cos(theta))*sin(7*phi)

#@torch.jit.script
def Yl38_m_minus_6(theta, phi):
    return 1.10139126615446e-9*(1.0 - cos(theta)**2)**3*(4.98417479060289e+19*cos(theta)**32 - 3.29620092818538e+20*cos(theta)**30 + 9.82087262849753e+20*cos(theta)**28 - 1.74285908618407e+21*cos(theta)**26 + 2.05227972105008e+21*cos(theta)**24 - 1.69083344182036e+21*cos(theta)**22 + 1.00149365400129e+21*cos(theta)**20 - 4.31482526667224e+20*cos(theta)**18 + 1.3528038233624e+20*cos(theta)**16 - 3.05718378160995e+19*cos(theta)**14 + 4.88076708993869e+18*cos(theta)**12 - 5.32447318902403e+17*cos(theta)**10 + 3.76731593563021e+16*cos(theta)**8 - 1.59102332123146e+15*cos(theta)**6 + 34789139677072.7*cos(theta)**4 - 296077784485.725*cos(theta)**2 + 411219145.119063)*sin(6*phi)

#@torch.jit.script
def Yl38_m_minus_5(theta, phi):
    return 4.1968643903827e-8*(1.0 - cos(theta)**2)**2.5*(1.51035599715239e+18*cos(theta)**33 - 1.06329062199528e+19*cos(theta)**31 + 3.38650780293018e+19*cos(theta)**29 - 6.45503365253359e+19*cos(theta)**27 + 8.20911888420032e+19*cos(theta)**25 - 7.35144974704506e+19*cos(theta)**23 + 4.76901740000616e+19*cos(theta)**21 - 2.2709606666696e+19*cos(theta)**19 + 7.9576695491906e+18*cos(theta)**17 - 2.0381225210733e+18*cos(theta)**15 + 3.75443622302976e+17*cos(theta)**13 - 4.84043017184002e+16*cos(theta)**11 + 4.18590659514467e+15*cos(theta)**9 - 227289045890209.0*cos(theta)**7 + 6957827935414.55*cos(theta)**5 - 98692594828.5751*cos(theta)**3 + 411219145.119063*cos(theta))*sin(5*phi)

#@torch.jit.script
def Yl38_m_minus_4(theta, phi):
    return 1.60471762562345e-6*(1.0 - cos(theta)**2)**2*(4.44222352103644e+16*cos(theta)**34 - 3.32278319373526e+17*cos(theta)**32 + 1.12883593431006e+18*cos(theta)**30 - 2.30536916161914e+18*cos(theta)**28 + 3.15735341700012e+18*cos(theta)**26 - 3.06310406126878e+18*cos(theta)**24 + 2.16773518182098e+18*cos(theta)**22 - 1.1354803333348e+18*cos(theta)**20 + 4.42092752732811e+17*cos(theta)**18 - 1.27382657567081e+17*cos(theta)**16 + 2.68174015930697e+16*cos(theta)**14 - 4.03369180986669e+15*cos(theta)**12 + 418590659514467.0*cos(theta)**10 - 28411130736276.1*cos(theta)**8 + 1159637989235.76*cos(theta)**6 - 24673148707.1438*cos(theta)**4 + 205609572.559532*cos(theta)**2 - 281271.645088278)*sin(4*phi)

#@torch.jit.script
def Yl38_m_minus_3(theta, phi):
    return 6.15258029386065e-5*(1.0 - cos(theta)**2)**1.5*(1.26920672029613e+15*cos(theta)**35 - 1.00690399810159e+16*cos(theta)**33 + 3.64140623970987e+16*cos(theta)**31 - 7.94954883316944e+16*cos(theta)**29 + 1.16939015444449e+17*cos(theta)**27 - 1.22524162450751e+17*cos(theta)**25 + 9.4249355731347e+16*cos(theta)**23 - 5.40704920635619e+16*cos(theta)**21 + 2.32680396175164e+16*cos(theta)**19 - 7.49309750394595e+15*cos(theta)**17 + 1.78782677287132e+15*cos(theta)**15 - 310283985374361.0*cos(theta)**13 + 38053696319497.0*cos(theta)**11 - 3156792304030.67*cos(theta)**9 + 165662569890.823*cos(theta)**7 - 4934629741.42876*cos(theta)**5 + 68536524.1865105*cos(theta)**3 - 281271.645088278*cos(theta))*sin(3*phi)

#@torch.jit.script
def Yl38_m_minus_2(theta, phi):
    return 0.00236374416014225*(1.0 - cos(theta)**2)*(35255742230448.0*cos(theta)**36 - 296148234735763.0*cos(theta)**34 + 1.13793944990934e+15*cos(theta)**32 - 2.64984961105648e+15*cos(theta)**30 + 4.17639340873032e+15*cos(theta)**28 - 4.71246778656735e+15*cos(theta)**26 + 3.92705648880612e+15*cos(theta)**24 - 2.45774963925281e+15*cos(theta)**22 + 1.16340198087582e+15*cos(theta)**20 - 416283194663664.0*cos(theta)**18 + 111739173304457.0*cos(theta)**16 - 22163141812454.3*cos(theta)**14 + 3171141359958.09*cos(theta)**12 - 315679230403.067*cos(theta)**10 + 20707821236.3528*cos(theta)**8 - 822438290.238126*cos(theta)**6 + 17134131.0466276*cos(theta)**4 - 140635.822544139*cos(theta)**2 + 190.56344518176)*sin(2*phi)

#@torch.jit.script
def Yl38_m_minus_1(theta, phi):
    return 0.090935053487738*(1.0 - cos(theta)**2)**0.5*(952857898120.215*cos(theta)**37 - 8461378135307.51*cos(theta)**35 + 34483013633616.2*cos(theta)**33 - 85479019711499.4*cos(theta)**31 + 144013565818287.0*cos(theta)**29 - 174535843946939.0*cos(theta)**27 + 157082259552245.0*cos(theta)**25 - 106858679967514.0*cos(theta)**23 + 55400094327420.0*cos(theta)**21 - 21909641824403.4*cos(theta)**19 + 6572892547321.01*cos(theta)**17 - 1477542787496.95*cos(theta)**15 + 243933950766.007*cos(theta)**13 - 28698111854.8243*cos(theta)**11 + 2300869026.26142*cos(theta)**9 - 117491184.319732*cos(theta)**7 + 3426826.20932553*cos(theta)**5 - 46878.6075147131*cos(theta)**3 + 190.56344518176*cos(theta))*sin(phi)

#@torch.jit.script
def Yl38_m0(theta, phi):
    return 195000104809.684*cos(theta)**38 - 1827800982416.11*cos(theta)**36 + 7887086430973.62*cos(theta)**34 - 20773030459043.2*cos(theta)**32 + 37331243143787.8*cos(theta)**30 - 48474897813575.2*cos(theta)**28 + 46983362496234.4*cos(theta)**26 - 34624927009696.6*cos(theta)**24 + 19582950521877.6*cos(theta)**22 - 8519136667709.45*cos(theta)**20 + 2839712222569.82*cos(theta)**18 - 718142099261.458*cos(theta)**16 + 135498509294.615*cos(theta)**14 - 18597834609.0648*cos(theta)**12 + 1789296041.10536*cos(theta)**10 - 114210385.602469*cos(theta)**8 + 4441514.99565159*cos(theta)**6 - 91139.1585975019*cos(theta)**4 + 740.968769085381*cos(theta)**2 - 0.999957853016709

#@torch.jit.script
def Yl38_m1(theta, phi):
    return 0.090935053487738*(1.0 - cos(theta)**2)**0.5*(952857898120.215*cos(theta)**37 - 8461378135307.51*cos(theta)**35 + 34483013633616.2*cos(theta)**33 - 85479019711499.4*cos(theta)**31 + 144013565818287.0*cos(theta)**29 - 174535843946939.0*cos(theta)**27 + 157082259552245.0*cos(theta)**25 - 106858679967514.0*cos(theta)**23 + 55400094327420.0*cos(theta)**21 - 21909641824403.4*cos(theta)**19 + 6572892547321.01*cos(theta)**17 - 1477542787496.95*cos(theta)**15 + 243933950766.007*cos(theta)**13 - 28698111854.8243*cos(theta)**11 + 2300869026.26142*cos(theta)**9 - 117491184.319732*cos(theta)**7 + 3426826.20932553*cos(theta)**5 - 46878.6075147131*cos(theta)**3 + 190.56344518176*cos(theta))*cos(phi)

#@torch.jit.script
def Yl38_m2(theta, phi):
    return 0.00236374416014225*(1.0 - cos(theta)**2)*(35255742230448.0*cos(theta)**36 - 296148234735763.0*cos(theta)**34 + 1.13793944990934e+15*cos(theta)**32 - 2.64984961105648e+15*cos(theta)**30 + 4.17639340873032e+15*cos(theta)**28 - 4.71246778656735e+15*cos(theta)**26 + 3.92705648880612e+15*cos(theta)**24 - 2.45774963925281e+15*cos(theta)**22 + 1.16340198087582e+15*cos(theta)**20 - 416283194663664.0*cos(theta)**18 + 111739173304457.0*cos(theta)**16 - 22163141812454.3*cos(theta)**14 + 3171141359958.09*cos(theta)**12 - 315679230403.067*cos(theta)**10 + 20707821236.3528*cos(theta)**8 - 822438290.238126*cos(theta)**6 + 17134131.0466276*cos(theta)**4 - 140635.822544139*cos(theta)**2 + 190.56344518176)*cos(2*phi)

#@torch.jit.script
def Yl38_m3(theta, phi):
    return 6.15258029386065e-5*(1.0 - cos(theta)**2)**1.5*(1.26920672029613e+15*cos(theta)**35 - 1.00690399810159e+16*cos(theta)**33 + 3.64140623970987e+16*cos(theta)**31 - 7.94954883316944e+16*cos(theta)**29 + 1.16939015444449e+17*cos(theta)**27 - 1.22524162450751e+17*cos(theta)**25 + 9.4249355731347e+16*cos(theta)**23 - 5.40704920635619e+16*cos(theta)**21 + 2.32680396175164e+16*cos(theta)**19 - 7.49309750394595e+15*cos(theta)**17 + 1.78782677287132e+15*cos(theta)**15 - 310283985374361.0*cos(theta)**13 + 38053696319497.0*cos(theta)**11 - 3156792304030.67*cos(theta)**9 + 165662569890.823*cos(theta)**7 - 4934629741.42876*cos(theta)**5 + 68536524.1865105*cos(theta)**3 - 281271.645088278*cos(theta))*cos(3*phi)

#@torch.jit.script
def Yl38_m4(theta, phi):
    return 1.60471762562345e-6*(1.0 - cos(theta)**2)**2*(4.44222352103644e+16*cos(theta)**34 - 3.32278319373526e+17*cos(theta)**32 + 1.12883593431006e+18*cos(theta)**30 - 2.30536916161914e+18*cos(theta)**28 + 3.15735341700012e+18*cos(theta)**26 - 3.06310406126878e+18*cos(theta)**24 + 2.16773518182098e+18*cos(theta)**22 - 1.1354803333348e+18*cos(theta)**20 + 4.42092752732811e+17*cos(theta)**18 - 1.27382657567081e+17*cos(theta)**16 + 2.68174015930697e+16*cos(theta)**14 - 4.03369180986669e+15*cos(theta)**12 + 418590659514467.0*cos(theta)**10 - 28411130736276.1*cos(theta)**8 + 1159637989235.76*cos(theta)**6 - 24673148707.1438*cos(theta)**4 + 205609572.559532*cos(theta)**2 - 281271.645088278)*cos(4*phi)

#@torch.jit.script
def Yl38_m5(theta, phi):
    return 4.1968643903827e-8*(1.0 - cos(theta)**2)**2.5*(1.51035599715239e+18*cos(theta)**33 - 1.06329062199528e+19*cos(theta)**31 + 3.38650780293018e+19*cos(theta)**29 - 6.45503365253359e+19*cos(theta)**27 + 8.20911888420032e+19*cos(theta)**25 - 7.35144974704506e+19*cos(theta)**23 + 4.76901740000616e+19*cos(theta)**21 - 2.2709606666696e+19*cos(theta)**19 + 7.9576695491906e+18*cos(theta)**17 - 2.0381225210733e+18*cos(theta)**15 + 3.75443622302976e+17*cos(theta)**13 - 4.84043017184002e+16*cos(theta)**11 + 4.18590659514467e+15*cos(theta)**9 - 227289045890209.0*cos(theta)**7 + 6957827935414.55*cos(theta)**5 - 98692594828.5751*cos(theta)**3 + 411219145.119063*cos(theta))*cos(5*phi)

#@torch.jit.script
def Yl38_m6(theta, phi):
    return 1.10139126615446e-9*(1.0 - cos(theta)**2)**3*(4.98417479060289e+19*cos(theta)**32 - 3.29620092818538e+20*cos(theta)**30 + 9.82087262849753e+20*cos(theta)**28 - 1.74285908618407e+21*cos(theta)**26 + 2.05227972105008e+21*cos(theta)**24 - 1.69083344182036e+21*cos(theta)**22 + 1.00149365400129e+21*cos(theta)**20 - 4.31482526667224e+20*cos(theta)**18 + 1.3528038233624e+20*cos(theta)**16 - 3.05718378160995e+19*cos(theta)**14 + 4.88076708993869e+18*cos(theta)**12 - 5.32447318902403e+17*cos(theta)**10 + 3.76731593563021e+16*cos(theta)**8 - 1.59102332123146e+15*cos(theta)**6 + 34789139677072.7*cos(theta)**4 - 296077784485.725*cos(theta)**2 + 411219145.119063)*cos(6*phi)

#@torch.jit.script
def Yl38_m7(theta, phi):
    return 2.90242083005401e-11*(1.0 - cos(theta)**2)**3.5*(1.59493593299292e+21*cos(theta)**31 - 9.88860278455613e+21*cos(theta)**29 + 2.74984433597931e+22*cos(theta)**27 - 4.53143362407858e+22*cos(theta)**25 + 4.92547133052019e+22*cos(theta)**23 - 3.7198335720048e+22*cos(theta)**21 + 2.00298730800259e+22*cos(theta)**19 - 7.76668548001003e+21*cos(theta)**17 + 2.16448611737984e+21*cos(theta)**15 - 4.28005729425393e+20*cos(theta)**13 + 5.85692050792643e+19*cos(theta)**11 - 5.32447318902403e+18*cos(theta)**9 + 3.01385274850417e+17*cos(theta)**7 - 9.54613992738876e+15*cos(theta)**5 + 139156558708291.0*cos(theta)**3 - 592155568971.451*cos(theta))*cos(7*phi)

#@torch.jit.script
def Yl38_m8(theta, phi):
    return 7.68600423582523e-13*(1.0 - cos(theta)**2)**4*(4.94430139227807e+22*cos(theta)**30 - 2.86769480752128e+23*cos(theta)**28 + 7.42457970714413e+23*cos(theta)**26 - 1.13285840601964e+24*cos(theta)**24 + 1.13285840601964e+24*cos(theta)**22 - 7.81165050121009e+23*cos(theta)**20 + 3.80567588520491e+23*cos(theta)**18 - 1.3203365316017e+23*cos(theta)**16 + 3.24672917606977e+22*cos(theta)**14 - 5.56407448253011e+21*cos(theta)**12 + 6.44261255871907e+20*cos(theta)**10 - 4.79202587012162e+19*cos(theta)**8 + 2.10969692395292e+18*cos(theta)**6 - 4.77306996369438e+16*cos(theta)**4 + 417469676124873.0*cos(theta)**2 - 592155568971.451)*cos(8*phi)

#@torch.jit.script
def Yl38_m9(theta, phi):
    return 2.04687378153282e-14*(1.0 - cos(theta)**2)**4.5*(1.48329041768342e+24*cos(theta)**29 - 8.02954546105958e+24*cos(theta)**27 + 1.93039072385747e+25*cos(theta)**25 - 2.71886017444715e+25*cos(theta)**23 + 2.49228849324322e+25*cos(theta)**21 - 1.56233010024202e+25*cos(theta)**19 + 6.85021659336884e+24*cos(theta)**17 - 2.11253845056273e+24*cos(theta)**15 + 4.54542084649767e+23*cos(theta)**13 - 6.67688937903613e+22*cos(theta)**11 + 6.44261255871907e+21*cos(theta)**9 - 3.8336206960973e+20*cos(theta)**7 + 1.26581815437175e+19*cos(theta)**5 - 1.90922798547775e+17*cos(theta)**3 + 834939352249746.0*cos(theta))*cos(9*phi)

#@torch.jit.script
def Yl38_m10(theta, phi):
    return 5.48619759603045e-16*(1.0 - cos(theta)**2)**5*(4.30154221128192e+25*cos(theta)**28 - 2.16797727448609e+26*cos(theta)**26 + 4.82597680964369e+26*cos(theta)**24 - 6.25337840122844e+26*cos(theta)**22 + 5.23380583581076e+26*cos(theta)**20 - 2.96842719045983e+26*cos(theta)**18 + 1.1645368208727e+26*cos(theta)**16 - 3.16880767584409e+25*cos(theta)**14 + 5.90904710044697e+24*cos(theta)**12 - 7.34457831693974e+23*cos(theta)**10 + 5.79835130284716e+22*cos(theta)**8 - 2.68353448726811e+21*cos(theta)**6 + 6.32909077185875e+19*cos(theta)**4 - 5.72768395643326e+17*cos(theta)**2 + 834939352249746.0)*cos(10*phi)

#@torch.jit.script
def Yl38_m11(theta, phi):
    return 1.48113413086296e-17*(1.0 - cos(theta)**2)**5.5*(1.20443181915894e+27*cos(theta)**27 - 5.63674091366382e+27*cos(theta)**25 + 1.15823443431448e+28*cos(theta)**23 - 1.37574324827026e+28*cos(theta)**21 + 1.04676116716215e+28*cos(theta)**19 - 5.3431689428277e+27*cos(theta)**17 + 1.86325891339633e+27*cos(theta)**15 - 4.43633074618173e+26*cos(theta)**13 + 7.09085652053637e+25*cos(theta)**11 - 7.34457831693974e+24*cos(theta)**9 + 4.63868104227773e+23*cos(theta)**7 - 1.61012069236087e+22*cos(theta)**5 + 2.5316363087435e+20*cos(theta)**3 - 1.14553679128665e+18*cos(theta))*cos(11*phi)

#@torch.jit.script
def Yl38_m12(theta, phi):
    return 4.03113651248321e-19*(1.0 - cos(theta)**2)**6*(3.25196591172913e+28*cos(theta)**26 - 1.40918522841596e+29*cos(theta)**24 + 2.66393919892331e+29*cos(theta)**22 - 2.88906082136754e+29*cos(theta)**20 + 1.98884621760809e+29*cos(theta)**18 - 9.08338720280709e+28*cos(theta)**16 + 2.79488837009449e+28*cos(theta)**14 - 5.76722997003625e+27*cos(theta)**12 + 7.79994217259e+26*cos(theta)**10 - 6.61012048524577e+25*cos(theta)**8 + 3.24707672959441e+24*cos(theta)**6 - 8.05060346180433e+22*cos(theta)**4 + 7.5949089262305e+20*cos(theta)**2 - 1.14553679128665e+18)*cos(12*phi)

#@torch.jit.script
def Yl38_m13(theta, phi):
    return 1.10702070454543e-20*(1.0 - cos(theta)**2)**6.5*(8.45511137049574e+29*cos(theta)**25 - 3.38204454819829e+30*cos(theta)**23 + 5.86066623763129e+30*cos(theta)**21 - 5.77812164273508e+30*cos(theta)**19 + 3.57992319169456e+30*cos(theta)**17 - 1.45334195244913e+30*cos(theta)**15 + 3.91284371813228e+29*cos(theta)**13 - 6.9206759640435e+28*cos(theta)**11 + 7.79994217259001e+27*cos(theta)**9 - 5.28809638819661e+26*cos(theta)**7 + 1.94824603775665e+25*cos(theta)**5 - 3.22024138472173e+23*cos(theta)**3 + 1.5189817852461e+21*cos(theta))*cos(13*phi)

#@torch.jit.script
def Yl38_m14(theta, phi):
    return 3.0703230101837e-22*(1.0 - cos(theta)**2)**7*(2.11377784262393e+31*cos(theta)**24 - 7.77870246085608e+31*cos(theta)**22 + 1.23073990990257e+32*cos(theta)**20 - 1.09784311211966e+32*cos(theta)**18 + 6.08586942588075e+31*cos(theta)**16 - 2.1800129286737e+31*cos(theta)**14 + 5.08669683357197e+30*cos(theta)**12 - 7.61274356044784e+29*cos(theta)**10 + 7.019947955331e+28*cos(theta)**8 - 3.70166747173763e+27*cos(theta)**6 + 9.74123018878324e+25*cos(theta)**4 - 9.66072415416519e+23*cos(theta)**2 + 1.5189817852461e+21)*cos(14*phi)

#@torch.jit.script
def Yl38_m15(theta, phi):
    return 8.60875824089541e-24*(1.0 - cos(theta)**2)**7.5*(5.07306682229744e+32*cos(theta)**23 - 1.71131454138834e+33*cos(theta)**21 + 2.46147981980514e+33*cos(theta)**19 - 1.9761176018154e+33*cos(theta)**17 + 9.7373910814092e+32*cos(theta)**15 - 3.05201810014318e+32*cos(theta)**13 + 6.10403620028636e+31*cos(theta)**11 - 7.61274356044785e+30*cos(theta)**9 + 5.6159583642648e+29*cos(theta)**7 - 2.22100048304258e+28*cos(theta)**5 + 3.89649207551329e+26*cos(theta)**3 - 1.93214483083304e+24*cos(theta))*cos(15*phi)

#@torch.jit.script
def Yl38_m16(theta, phi):
    return 2.44275389142847e-25*(1.0 - cos(theta)**2)**8*(1.16680536912841e+34*cos(theta)**22 - 3.59376053691551e+34*cos(theta)**20 + 4.67681165762977e+34*cos(theta)**18 - 3.35939992308617e+34*cos(theta)**16 + 1.46060866221138e+34*cos(theta)**14 - 3.96762353018614e+33*cos(theta)**12 + 6.714439820315e+32*cos(theta)**10 - 6.85146920440306e+31*cos(theta)**8 + 3.93117085498536e+30*cos(theta)**6 - 1.11050024152129e+29*cos(theta)**4 + 1.16894762265399e+27*cos(theta)**2 - 1.93214483083304e+24)*cos(16*phi)

#@torch.jit.script
def Yl38_m17(theta, phi):
    return 7.02242369104875e-27*(1.0 - cos(theta)**2)**8.5*(2.56697181208251e+35*cos(theta)**21 - 7.18752107383102e+35*cos(theta)**19 + 8.41826098373359e+35*cos(theta)**17 - 5.37503987693788e+35*cos(theta)**15 + 2.04485212709593e+35*cos(theta)**13 - 4.76114823622336e+34*cos(theta)**11 + 6.714439820315e+33*cos(theta)**9 - 5.48117536352245e+32*cos(theta)**7 + 2.35870251299122e+31*cos(theta)**5 - 4.44200096608516e+29*cos(theta)**3 + 2.33789524530798e+27*cos(theta))*cos(17*phi)

#@torch.jit.script
def Yl38_m18(theta, phi):
    return 2.04778033341685e-28*(1.0 - cos(theta)**2)**9*(5.39064080537326e+36*cos(theta)**20 - 1.36562900402789e+37*cos(theta)**18 + 1.43110436723471e+37*cos(theta)**16 - 8.06255981540682e+36*cos(theta)**14 + 2.65830776522471e+36*cos(theta)**12 - 5.2372630598457e+35*cos(theta)**10 + 6.0429958382835e+34*cos(theta)**8 - 3.83682275446571e+33*cos(theta)**6 + 1.17935125649561e+32*cos(theta)**4 - 1.33260028982555e+30*cos(theta)**2 + 2.33789524530798e+27)*cos(18*phi)

#@torch.jit.script
def Yl38_m19(theta, phi):
    return 6.06500191198304e-30*(1.0 - cos(theta)**2)**9.5*(1.07812816107465e+38*cos(theta)**19 - 2.45813220725021e+38*cos(theta)**17 + 2.28976698757554e+38*cos(theta)**15 - 1.12875837415695e+38*cos(theta)**13 + 3.18996931826965e+37*cos(theta)**11 - 5.2372630598457e+36*cos(theta)**9 + 4.8343966706268e+35*cos(theta)**7 - 2.30209365267943e+34*cos(theta)**5 + 4.71740502598244e+32*cos(theta)**3 - 2.66520057965109e+30*cos(theta))*cos(19*phi)

#@torch.jit.script
def Yl38_m20(theta, phi):
    return 1.82700672042423e-31*(1.0 - cos(theta)**2)**10*(2.04844350604184e+39*cos(theta)**18 - 4.17882475232535e+39*cos(theta)**16 + 3.4346504813633e+39*cos(theta)**14 - 1.46738588640404e+39*cos(theta)**12 + 3.50896625009662e+38*cos(theta)**10 - 4.71353675386113e+37*cos(theta)**8 + 3.38407766943876e+36*cos(theta)**6 - 1.15104682633971e+35*cos(theta)**4 + 1.41522150779473e+33*cos(theta)**2 - 2.66520057965109e+30)*cos(20*phi)

#@torch.jit.script
def Yl38_m21(theta, phi):
    return 5.60632004517403e-33*(1.0 - cos(theta)**2)**10.5*(3.68719831087531e+40*cos(theta)**17 - 6.68611960372056e+40*cos(theta)**15 + 4.80851067390862e+40*cos(theta)**13 - 1.76086306368485e+40*cos(theta)**11 + 3.50896625009662e+39*cos(theta)**9 - 3.7708294030889e+38*cos(theta)**7 + 2.03044660166326e+37*cos(theta)**5 - 4.60418730535886e+35*cos(theta)**3 + 2.83044301558946e+33*cos(theta))*cos(21*phi)

#@torch.jit.script
def Yl38_m22(theta, phi):
    return 1.75540689794278e-34*(1.0 - cos(theta)**2)**11*(6.26823712848803e+41*cos(theta)**16 - 1.00291794055808e+42*cos(theta)**14 + 6.25106387608121e+41*cos(theta)**12 - 1.93694937005333e+41*cos(theta)**10 + 3.15806962508696e+40*cos(theta)**8 - 2.63958058216223e+39*cos(theta)**6 + 1.01522330083163e+38*cos(theta)**4 - 1.38125619160766e+36*cos(theta)**2 + 2.83044301558946e+33)*cos(22*phi)

#@torch.jit.script
def Yl38_m23(theta, phi):
    return 5.61892055563194e-36*(1.0 - cos(theta)**2)**11.5*(1.00291794055808e+43*cos(theta)**15 - 1.40408511678132e+43*cos(theta)**13 + 7.50127665129745e+42*cos(theta)**11 - 1.93694937005333e+42*cos(theta)**9 + 2.52645570006957e+41*cos(theta)**7 - 1.58374834929734e+40*cos(theta)**5 + 4.06089320332651e+38*cos(theta)**3 - 2.76251238321531e+36*cos(theta))*cos(23*phi)

#@torch.jit.script
def Yl38_m24(theta, phi):
    return 1.84251663480048e-37*(1.0 - cos(theta)**2)**12*(1.50437691083713e+44*cos(theta)**14 - 1.82531065181571e+44*cos(theta)**12 + 8.2514043164272e+43*cos(theta)**10 - 1.743254433048e+43*cos(theta)**8 + 1.7685189900487e+42*cos(theta)**6 - 7.9187417464867e+40*cos(theta)**4 + 1.21826796099795e+39*cos(theta)**2 - 2.76251238321531e+36)*cos(24*phi)

#@torch.jit.script
def Yl38_m25(theta, phi):
    return 6.20407622341159e-39*(1.0 - cos(theta)**2)**12.5*(2.10612767517198e+45*cos(theta)**13 - 2.19037278217886e+45*cos(theta)**11 + 8.2514043164272e+44*cos(theta)**9 - 1.3946035464384e+44*cos(theta)**7 + 1.06111139402922e+43*cos(theta)**5 - 3.16749669859468e+41*cos(theta)**3 + 2.43653592199591e+39*cos(theta))*cos(25*phi)

#@torch.jit.script
def Yl38_m26(theta, phi):
    return 2.15087643657668e-40*(1.0 - cos(theta)**2)**13*(2.73796597772357e+46*cos(theta)**12 - 2.40941006039674e+46*cos(theta)**10 + 7.42626388478448e+45*cos(theta)**8 - 9.7622248250688e+44*cos(theta)**6 + 5.30555697014609e+43*cos(theta)**4 - 9.50249009578404e+41*cos(theta)**2 + 2.43653592199591e+39)*cos(26*phi)

#@torch.jit.script
def Yl38_m27(theta, phi):
    return 7.70137304226747e-42*(1.0 - cos(theta)**2)**13.5*(3.28555917326829e+47*cos(theta)**11 - 2.40941006039674e+47*cos(theta)**9 + 5.94101110782758e+46*cos(theta)**7 - 5.85733489504128e+45*cos(theta)**5 + 2.12222278805844e+44*cos(theta)**3 - 1.90049801915681e+42*cos(theta))*cos(27*phi)

#@torch.jit.script
def Yl38_m28(theta, phi):
    return 2.85824761702743e-43*(1.0 - cos(theta)**2)**14*(3.61411509059511e+48*cos(theta)**10 - 2.16846905435707e+48*cos(theta)**8 + 4.15870777547931e+47*cos(theta)**6 - 2.92866744752064e+46*cos(theta)**4 + 6.3666683641753e+44*cos(theta)**2 - 1.90049801915681e+42)*cos(28*phi)

#@torch.jit.script
def Yl38_m29(theta, phi):
    return 1.1042373906736e-44*(1.0 - cos(theta)**2)**14.5*(3.61411509059511e+49*cos(theta)**9 - 1.73477524348565e+49*cos(theta)**7 + 2.49522466528759e+48*cos(theta)**5 - 1.17146697900826e+47*cos(theta)**3 + 1.27333367283506e+45*cos(theta))*cos(29*phi)

#@torch.jit.script
def Yl38_m30(theta, phi):
    return 4.46361509559185e-46*(1.0 - cos(theta)**2)**15*(3.2527035815356e+50*cos(theta)**8 - 1.21434267043996e+50*cos(theta)**6 + 1.24761233264379e+49*cos(theta)**4 - 3.51440093702477e+47*cos(theta)**2 + 1.27333367283506e+45)*cos(30*phi)

#@torch.jit.script
def Yl38_m31(theta, phi):
    return 1.89984075045795e-47*(1.0 - cos(theta)**2)**15.5*(2.60216286522848e+51*cos(theta)**7 - 7.28605602263975e+50*cos(theta)**5 + 4.99044933057517e+49*cos(theta)**3 - 7.02880187404954e+47*cos(theta))*cos(31*phi)

#@torch.jit.script
def Yl38_m32(theta, phi):
    return 8.58260566150099e-49*(1.0 - cos(theta)**2)**16*(1.82151400565994e+52*cos(theta)**6 - 3.64302801131987e+51*cos(theta)**4 + 1.49713479917255e+50*cos(theta)**2 - 7.02880187404954e+47)*cos(32*phi)

#@torch.jit.script
def Yl38_m33(theta, phi):
    return 4.15828603021903e-50*(1.0 - cos(theta)**2)**16.5*(1.09290840339596e+53*cos(theta)**5 - 1.45721120452795e+52*cos(theta)**3 + 2.9942695983451e+50*cos(theta))*cos(33*phi)

#@torch.jit.script
def Yl38_m34(theta, phi):
    return 2.19160916965865e-51*(1.0 - cos(theta)**2)**17*(5.46454201697981e+53*cos(theta)**4 - 4.37163361358385e+52*cos(theta)**2 + 2.9942695983451e+50)*cos(34*phi)

#@torch.jit.script
def Yl38_m35(theta, phi):
    return 1.28254225711204e-52*(1.0 - cos(theta)**2)**17.5*(2.18581680679192e+54*cos(theta)**3 - 8.7432672271677e+52*cos(theta))*cos(35*phi)

#@torch.jit.script
def Yl38_m36(theta, phi):
    return 8.60786001928606e-54*(1.0 - cos(theta)**2)**18*(6.55745042037577e+54*cos(theta)**2 - 8.7432672271677e+52)*cos(36*phi)

#@torch.jit.script
def Yl38_m37(theta, phi):
    return 9.21753038048947*(1.0 - cos(theta)**2)**18.5*cos(37*phi)*cos(theta)

#@torch.jit.script
def Yl38_m38(theta, phi):
    return 1.0573232483571*(1.0 - cos(theta)**2)**19*cos(38*phi)

#@torch.jit.script
def Yl39_m_minus_39(theta, phi):
    return 1.064079376195*(1.0 - cos(theta)**2)**19.5*sin(39*phi)

#@torch.jit.script
def Yl39_m_minus_38(theta, phi):
    return 9.39769459334552*(1.0 - cos(theta)**2)**19*sin(38*phi)*cos(theta)

#@torch.jit.script
def Yl39_m_minus_37(theta, phi):
    return 1.15485099036113e-55*(1.0 - cos(theta)**2)**18.5*(5.04923682368935e+56*cos(theta)**2 - 6.55745042037577e+54)*sin(37*phi)

#@torch.jit.script
def Yl39_m_minus_36(theta, phi):
    return 1.743786754927e-54*(1.0 - cos(theta)**2)**18*(1.68307894122978e+56*cos(theta)**3 - 6.55745042037577e+54*cos(theta))*sin(36*phi)

#@torch.jit.script
def Yl39_m_minus_35(theta, phi):
    return 3.02032725709922e-53*(1.0 - cos(theta)**2)**17.5*(4.20769735307446e+55*cos(theta)**4 - 3.27872521018789e+54*cos(theta)**2 + 2.18581680679192e+52)*sin(35*phi)

#@torch.jit.script
def Yl39_m_minus_34(theta, phi):
    return 5.80971547822379e-52*(1.0 - cos(theta)**2)**17*(8.41539470614891e+54*cos(theta)**5 - 1.09290840339596e+54*cos(theta)**3 + 2.18581680679192e+52*cos(theta))*sin(34*phi)

#@torch.jit.script
def Yl39_m_minus_33(theta, phi):
    return 1.21588337207176e-50*(1.0 - cos(theta)**2)**16.5*(1.40256578435815e+54*cos(theta)**6 - 2.73227100848991e+53*cos(theta)**4 + 1.09290840339596e+52*cos(theta)**2 - 4.99044933057517e+49)*sin(33*phi)

#@torch.jit.script
def Yl39_m_minus_32(theta, phi):
    return 2.72965140034074e-49*(1.0 - cos(theta)**2)**16*(2.00366540622593e+53*cos(theta)**7 - 5.46454201697981e+52*cos(theta)**5 + 3.64302801131987e+51*cos(theta)**3 - 4.99044933057517e+49*cos(theta))*sin(32*phi)

#@torch.jit.script
def Yl39_m_minus_31(theta, phi):
    return 6.50551009827291e-48*(1.0 - cos(theta)**2)**15.5*(2.50458175778241e+52*cos(theta)**8 - 9.10757002829969e+51*cos(theta)**6 + 9.10757002829969e+50*cos(theta)**4 - 2.49522466528759e+49*cos(theta)**2 + 8.78600234256192e+46)*sin(31*phi)

#@torch.jit.script
def Yl39_m_minus_30(theta, phi):
    return 1.63287007543161e-46*(1.0 - cos(theta)**2)**15*(2.78286861975824e+51*cos(theta)**9 - 1.30108143261424e+51*cos(theta)**7 + 1.82151400565994e+50*cos(theta)**5 - 8.31741555095862e+48*cos(theta)**3 + 8.78600234256192e+46*cos(theta))*sin(30*phi)

#@torch.jit.script
def Yl39_m_minus_29(theta, phi):
    return 4.28919879632039e-45*(1.0 - cos(theta)**2)**14.5*(2.78286861975824e+50*cos(theta)**10 - 1.6263517907678e+50*cos(theta)**8 + 3.0358566760999e+49*cos(theta)**6 - 2.07935388773965e+48*cos(theta)**4 + 4.39300117128096e+46*cos(theta)**2 - 1.27333367283506e+44)*sin(29*phi)

#@torch.jit.script
def Yl39_m_minus_28(theta, phi):
    return 1.1730782277043e-43*(1.0 - cos(theta)**2)**14*(2.52988056341658e+49*cos(theta)**11 - 1.80705754529756e+49*cos(theta)**9 + 4.33693810871414e+48*cos(theta)**7 - 4.15870777547931e+47*cos(theta)**5 + 1.46433372376032e+46*cos(theta)**3 - 1.27333367283506e+44*cos(theta))*sin(28*phi)

#@torch.jit.script
def Yl39_m_minus_27(theta, phi):
    return 3.326250851581e-42*(1.0 - cos(theta)**2)**13.5*(2.10823380284715e+48*cos(theta)**12 - 1.80705754529756e+48*cos(theta)**10 + 5.42117263589267e+47*cos(theta)**8 - 6.93117962579885e+46*cos(theta)**6 + 3.6608343094008e+45*cos(theta)**4 - 6.3666683641753e+43*cos(theta)**2 + 1.58374834929734e+41)*sin(27*phi)

#@torch.jit.script
def Yl39_m_minus_26(theta, phi):
    return 9.74313326210721e-41*(1.0 - cos(theta)**2)**13*(1.62171830988242e+47*cos(theta)**13 - 1.64277958663414e+47*cos(theta)**11 + 6.02352515099186e+46*cos(theta)**9 - 9.90168517971264e+45*cos(theta)**7 + 7.3216686188016e+44*cos(theta)**5 - 2.12222278805844e+43*cos(theta)**3 + 1.58374834929734e+41*cos(theta))*sin(26*phi)

#@torch.jit.script
def Yl39_m_minus_25(theta, phi):
    return 2.93913367583875e-39*(1.0 - cos(theta)**2)**12.5*(1.15837022134459e+46*cos(theta)**14 - 1.36898298886179e+46*cos(theta)**12 + 6.02352515099186e+45*cos(theta)**10 - 1.23771064746408e+45*cos(theta)**8 + 1.2202781031336e+44*cos(theta)**6 - 5.30555697014609e+42*cos(theta)**4 + 7.9187417464867e+40*cos(theta)**2 - 1.74038280142565e+38)*sin(25*phi)

#@torch.jit.script
def Yl39_m_minus_24(theta, phi):
    return 9.10657262304068e-38*(1.0 - cos(theta)**2)**12*(7.72246814229725e+44*cos(theta)**15 - 1.05306383758599e+45*cos(theta)**13 + 5.47593195544714e+44*cos(theta)**11 - 1.37523405273787e+44*cos(theta)**9 + 1.743254433048e+43*cos(theta)**7 - 1.06111139402922e+42*cos(theta)**5 + 2.63958058216223e+40*cos(theta)**3 - 1.74038280142565e+38*cos(theta))*sin(24*phi)

#@torch.jit.script
def Yl39_m_minus_23(theta, phi):
    return 2.89124717480577e-36*(1.0 - cos(theta)**2)**11.5*(4.82654258893578e+43*cos(theta)**16 - 7.52188455418563e+43*cos(theta)**14 + 4.56327662953929e+43*cos(theta)**12 - 1.37523405273787e+43*cos(theta)**10 + 2.17906804131e+42*cos(theta)**8 - 1.7685189900487e+41*cos(theta)**6 + 6.59895145540558e+39*cos(theta)**4 - 8.70191400712824e+37*cos(theta)**2 + 1.72657023950957e+35)*sin(23*phi)

#@torch.jit.script
def Yl39_m_minus_22(theta, phi):
    return 9.38653981934599e-35*(1.0 - cos(theta)**2)**11*(2.83914269937399e+42*cos(theta)**17 - 5.01458970279042e+42*cos(theta)**15 + 3.5102127919533e+42*cos(theta)**13 - 1.25021277521624e+42*cos(theta)**11 + 2.42118671256667e+41*cos(theta)**9 - 2.52645570006957e+40*cos(theta)**7 + 1.31979029108112e+39*cos(theta)**5 - 2.90063800237608e+37*cos(theta)**3 + 1.72657023950957e+35*cos(theta))*sin(22*phi)

#@torch.jit.script
def Yl39_m_minus_21(theta, phi):
    return 3.1103316302064e-33*(1.0 - cos(theta)**2)**10.5*(1.57730149965222e+41*cos(theta)**18 - 3.13411856424401e+41*cos(theta)**16 + 2.50729485139521e+41*cos(theta)**14 - 1.04184397934687e+41*cos(theta)**12 + 2.42118671256667e+40*cos(theta)**10 - 3.15806962508696e+39*cos(theta)**8 + 2.19965048513519e+38*cos(theta)**6 - 7.2515950059402e+36*cos(theta)**4 + 8.63285119754786e+34*cos(theta)**2 - 1.57246834199415e+32)*sin(21*phi)

#@torch.jit.script
def Yl39_m_minus_20(theta, phi):
    return 1.05016882684848e-31*(1.0 - cos(theta)**2)**10*(8.30158684027482e+39*cos(theta)**19 - 1.84359915543766e+40*cos(theta)**17 + 1.67152990093014e+40*cos(theta)**15 - 8.01418445651438e+39*cos(theta)**13 + 2.20107882960606e+39*cos(theta)**11 - 3.50896625009662e+38*cos(theta)**9 + 3.14235783590742e+37*cos(theta)**7 - 1.45031900118804e+36*cos(theta)**5 + 2.87761706584929e+34*cos(theta)**3 - 1.57246834199415e+32*cos(theta))*sin(20*phi)

#@torch.jit.script
def Yl39_m_minus_19(theta, phi):
    return 3.60744838710617e-30*(1.0 - cos(theta)**2)**9.5*(4.15079342013741e+38*cos(theta)**20 - 1.02422175302092e+39*cos(theta)**18 + 1.04470618808134e+39*cos(theta)**16 - 5.72441746893884e+38*cos(theta)**14 + 1.83423235800505e+38*cos(theta)**12 - 3.50896625009662e+37*cos(theta)**10 + 3.92794729488427e+36*cos(theta)**8 - 2.4171983353134e+35*cos(theta)**6 + 7.19404266462321e+33*cos(theta)**4 - 7.86234170997073e+31*cos(theta)**2 + 1.33260028982555e+29)*sin(19*phi)

#@torch.jit.script
def Yl39_m_minus_18(theta, phi):
    return 1.25899431882528e-28*(1.0 - cos(theta)**2)**9*(1.97656829530353e+37*cos(theta)**21 - 5.39064080537326e+37*cos(theta)**19 + 6.14533051812552e+37*cos(theta)**17 - 3.81627831262589e+37*cos(theta)**15 + 1.41094796769619e+37*cos(theta)**13 - 3.18996931826965e+36*cos(theta)**11 + 4.36438588320475e+35*cos(theta)**9 - 3.45314047901914e+34*cos(theta)**7 + 1.43880853292464e+33*cos(theta)**5 - 2.62078056999024e+31*cos(theta)**3 + 1.33260028982555e+29*cos(theta))*sin(18*phi)

#@torch.jit.script
def Yl39_m_minus_17(theta, phi):
    return 4.45833336048602e-27*(1.0 - cos(theta)**2)**8.5*(8.98440134228877e+35*cos(theta)**22 - 2.69532040268663e+36*cos(theta)**20 + 3.41407251006973e+36*cos(theta)**18 - 2.38517394539118e+36*cos(theta)**16 + 1.00781997692585e+36*cos(theta)**14 - 2.65830776522471e+35*cos(theta)**12 + 4.36438588320475e+34*cos(theta)**10 - 4.31642559877393e+33*cos(theta)**8 + 2.39801422154107e+32*cos(theta)**6 - 6.5519514249756e+30*cos(theta)**4 + 6.66300144912773e+28*cos(theta)**2 - 1.06267965695817e+26)*sin(17*phi)

#@torch.jit.script
def Yl39_m_minus_16(theta, phi):
    return 1.60003863775068e-25*(1.0 - cos(theta)**2)**8*(3.90626145316903e+34*cos(theta)**23 - 1.28348590604125e+35*cos(theta)**21 + 1.79688026845775e+35*cos(theta)**19 - 1.40304349728893e+35*cos(theta)**17 + 6.71879984617235e+34*cos(theta)**15 - 2.04485212709593e+34*cos(theta)**13 + 3.96762353018614e+33*cos(theta)**11 - 4.79602844308214e+32*cos(theta)**9 + 3.42573460220153e+31*cos(theta)**7 - 1.31039028499512e+30*cos(theta)**5 + 2.22100048304258e+28*cos(theta)**3 - 1.06267965695817e+26*cos(theta))*sin(16*phi)

#@torch.jit.script
def Yl39_m_minus_15(theta, phi):
    return 5.81322905778663e-24*(1.0 - cos(theta)**2)**7.5*(1.62760893882043e+33*cos(theta)**24 - 5.83402684564206e+33*cos(theta)**22 + 8.98440134228877e+33*cos(theta)**20 - 7.79468609604962e+33*cos(theta)**18 + 4.19924990385772e+33*cos(theta)**16 - 1.46060866221138e+33*cos(theta)**14 + 3.30635294182178e+32*cos(theta)**12 - 4.79602844308214e+31*cos(theta)**10 + 4.28216825275191e+30*cos(theta)**8 - 2.1839838083252e+29*cos(theta)**6 + 5.55250120760644e+27*cos(theta)**4 - 5.31339828479086e+25*cos(theta)**2 + 8.05060346180433e+22)*sin(15*phi)

#@torch.jit.script
def Yl39_m_minus_14(theta, phi):
    return 2.13591674242462e-22*(1.0 - cos(theta)**2)**7*(6.51043575528172e+31*cos(theta)**25 - 2.53653341114872e+32*cos(theta)**23 + 4.27828635347084e+32*cos(theta)**21 - 4.1024663663419e+32*cos(theta)**19 + 2.47014700226925e+32*cos(theta)**17 - 9.7373910814092e+31*cos(theta)**15 + 2.54334841678598e+31*cos(theta)**13 - 4.3600258573474e+30*cos(theta)**11 + 4.7579647252799e+29*cos(theta)**9 - 3.119976869036e+28*cos(theta)**7 + 1.11050024152129e+27*cos(theta)**5 - 1.77113276159695e+25*cos(theta)**3 + 8.05060346180433e+22*cos(theta))*sin(14*phi)

#@torch.jit.script
def Yl39_m_minus_13(theta, phi):
    return 7.92882675780294e-21*(1.0 - cos(theta)**2)**6.5*(2.50401375203143e+30*cos(theta)**26 - 1.05688892131197e+31*cos(theta)**24 + 1.94467561521402e+31*cos(theta)**22 - 2.05123318317095e+31*cos(theta)**20 + 1.37230389014958e+31*cos(theta)**18 - 6.08586942588075e+30*cos(theta)**16 + 1.81667744056142e+30*cos(theta)**14 - 3.63335488112284e+29*cos(theta)**12 + 4.7579647252799e+28*cos(theta)**10 - 3.899971086295e+27*cos(theta)**8 + 1.85083373586881e+26*cos(theta)**6 - 4.42783190399238e+24*cos(theta)**4 + 4.02530173090216e+22*cos(theta)**2 - 5.84223763556192e+19)*sin(13*phi)

#@torch.jit.script
def Yl39_m_minus_12(theta, phi):
    return 2.97093043392762e-19*(1.0 - cos(theta)**2)**6*(9.27412500752381e+28*cos(theta)**27 - 4.22755568524787e+29*cos(theta)**25 + 8.45511137049574e+29*cos(theta)**23 - 9.76777706271882e+29*cos(theta)**21 + 7.22265205341885e+29*cos(theta)**19 - 3.57992319169456e+29*cos(theta)**17 + 1.21111829370761e+29*cos(theta)**15 - 2.79488837009449e+28*cos(theta)**13 + 4.32542247752718e+27*cos(theta)**11 - 4.33330120699445e+26*cos(theta)**9 + 2.64404819409831e+25*cos(theta)**7 - 8.85566380798476e+23*cos(theta)**5 + 1.34176724363405e+22*cos(theta)**3 - 5.84223763556192e+19*cos(theta))*sin(12*phi)

#@torch.jit.script
def Yl39_m_minus_11(theta, phi):
    return 1.12268155211275e-17*(1.0 - cos(theta)**2)**5.5*(3.31218750268708e+27*cos(theta)**28 - 1.62598295586456e+28*cos(theta)**26 + 3.52296307103989e+28*cos(theta)**24 - 4.43989866487219e+28*cos(theta)**22 + 3.61132602670942e+28*cos(theta)**20 - 1.98884621760809e+28*cos(theta)**18 + 7.56948933567257e+27*cos(theta)**16 - 1.99634883578178e+27*cos(theta)**14 + 3.60451873127265e+26*cos(theta)**12 - 4.33330120699445e+25*cos(theta)**10 + 3.30506024262288e+24*cos(theta)**8 - 1.47594396799746e+23*cos(theta)**6 + 3.35441810908514e+21*cos(theta)**4 - 2.92111881778096e+19*cos(theta)**2 + 4.09120282602375e+16)*sin(11*phi)

#@torch.jit.script
def Yl39_m_minus_10(theta, phi):
    return 4.27504398551492e-16*(1.0 - cos(theta)**2)**5*(1.14213362161623e+26*cos(theta)**29 - 6.02215909579468e+26*cos(theta)**27 + 1.40918522841596e+27*cos(theta)**25 - 1.93039072385747e+27*cos(theta)**23 + 1.71967906033782e+27*cos(theta)**21 - 1.04676116716215e+27*cos(theta)**19 + 4.45264078568975e+26*cos(theta)**17 - 1.33089922385452e+26*cos(theta)**15 + 2.77270671636358e+25*cos(theta)**13 - 3.93936473363132e+24*cos(theta)**11 + 3.67228915846987e+23*cos(theta)**9 - 2.10849138285351e+22*cos(theta)**7 + 6.70883621817027e+20*cos(theta)**5 - 9.73706272593654e+18*cos(theta)**3 + 4.09120282602375e+16*cos(theta))*sin(10*phi)

#@torch.jit.script
def Yl39_m_minus_9(theta, phi):
    return 1.63907661763532e-14*(1.0 - cos(theta)**2)**4.5*(3.80711207205411e+24*cos(theta)**30 - 2.15077110564096e+25*cos(theta)**28 + 5.41994318621522e+25*cos(theta)**26 - 8.04329468273948e+25*cos(theta)**24 + 7.81672300153555e+25*cos(theta)**22 - 5.23380583581076e+25*cos(theta)**20 + 2.47368932538319e+25*cos(theta)**18 - 8.31812014909074e+24*cos(theta)**16 + 1.98050479740256e+24*cos(theta)**14 - 3.28280394469276e+23*cos(theta)**12 + 3.67228915846987e+22*cos(theta)**10 - 2.63561422856689e+21*cos(theta)**8 + 1.11813936969505e+20*cos(theta)**6 - 2.43426568148413e+18*cos(theta)**4 + 2.04560141301188e+16*cos(theta)**2 - 27831311741658.2)*sin(9*phi)

#@torch.jit.script
def Yl39_m_minus_8(theta, phi):
    return 6.32267298839384e-13*(1.0 - cos(theta)**2)**4*(1.22810066840455e+23*cos(theta)**31 - 7.4164520884171e+23*cos(theta)**29 + 2.00738636526489e+24*cos(theta)**27 - 3.21731787309579e+24*cos(theta)**25 + 3.39857521805893e+24*cos(theta)**23 - 2.49228849324322e+24*cos(theta)**21 + 1.30194175020168e+24*cos(theta)**19 - 4.89301185240632e+23*cos(theta)**17 + 1.3203365316017e+23*cos(theta)**15 - 2.52523380360982e+22*cos(theta)**13 + 3.33844468951806e+21*cos(theta)**11 - 2.92846025396321e+20*cos(theta)**9 + 1.59734195670721e+19*cos(theta)**7 - 4.86853136296827e+17*cos(theta)**5 + 6.81867137670626e+15*cos(theta)**3 - 27831311741658.2*cos(theta))*sin(8*phi)

#@torch.jit.script
def Yl39_m_minus_7(theta, phi):
    return 2.45202355926937e-11*(1.0 - cos(theta)**2)**3.5*(3.83781458876422e+21*cos(theta)**32 - 2.47215069613903e+22*cos(theta)**30 + 7.1692370188032e+22*cos(theta)**28 - 1.23742995119069e+23*cos(theta)**26 + 1.41607300752456e+23*cos(theta)**24 - 1.13285840601964e+23*cos(theta)**22 + 6.5097087510084e+22*cos(theta)**20 - 2.71833991800351e+22*cos(theta)**18 + 8.25210332251065e+21*cos(theta)**16 - 1.80373843114987e+21*cos(theta)**14 + 2.78203724126505e+20*cos(theta)**12 - 2.92846025396321e+19*cos(theta)**10 + 1.99667744588401e+18*cos(theta)**8 - 8.11421893828044e+16*cos(theta)**6 + 1.70466784417656e+15*cos(theta)**4 - 13915655870829.1*cos(theta)**2 + 18504861530.3578)*sin(7*phi)

#@torch.jit.script
def Yl39_m_minus_6(theta, phi):
    return 9.55345636639005e-10*(1.0 - cos(theta)**2)**3*(1.16297411780734e+20*cos(theta)**33 - 7.97467966496462e+20*cos(theta)**31 + 2.47215069613903e+21*cos(theta)**29 - 4.58307389329885e+21*cos(theta)**27 + 5.66429203009822e+21*cos(theta)**25 - 4.92547133052019e+21*cos(theta)**23 + 3.099861310004e+21*cos(theta)**21 - 1.43070522000185e+21*cos(theta)**19 + 4.85417842500627e+20*cos(theta)**17 - 1.20249228743325e+20*cos(theta)**15 + 2.14002864712696e+19*cos(theta)**13 - 2.66223659451201e+18*cos(theta)**11 + 2.21853049542668e+17*cos(theta)**9 - 1.15917413404006e+16*cos(theta)**7 + 340933568835313.0*cos(theta)**5 - 4638551956943.03*cos(theta)**3 + 18504861530.3578*cos(theta))*sin(6*phi)

#@torch.jit.script
def Yl39_m_minus_5(theta, phi):
    return 3.73685494330611e-8*(1.0 - cos(theta)**2)**2.5*(3.42051211119806e+18*cos(theta)**34 - 2.49208739530144e+19*cos(theta)**32 + 8.24050232046344e+19*cos(theta)**30 - 1.63681210474959e+20*cos(theta)**28 + 2.17857385773009e+20*cos(theta)**26 - 2.05227972105008e+20*cos(theta)**24 + 1.40902786818364e+20*cos(theta)**22 - 7.15352610000924e+19*cos(theta)**20 + 2.69676579167015e+19*cos(theta)**18 - 7.51557679645779e+18*cos(theta)**16 + 1.52859189080497e+18*cos(theta)**14 - 2.21853049542668e+17*cos(theta)**12 + 2.21853049542668e+16*cos(theta)**10 - 1.44896766755008e+15*cos(theta)**8 + 56822261472552.1*cos(theta)**6 - 1159637989235.76*cos(theta)**4 + 9252430765.17892*cos(theta)**2 - 12094680.738796)*sin(5*phi)

#@torch.jit.script
def Yl39_m_minus_4(theta, phi):
    return 1.46644777253264e-6*(1.0 - cos(theta)**2)**2*(9.77289174628017e+16*cos(theta)**35 - 7.55177998576195e+17*cos(theta)**33 + 2.65822655498821e+18*cos(theta)**31 - 5.6441796715503e+18*cos(theta)**29 + 8.06879206566698e+18*cos(theta)**27 - 8.20911888420032e+18*cos(theta)**25 + 6.12620812253755e+18*cos(theta)**23 - 3.4064410000044e+18*cos(theta)**21 + 1.4193504166685e+18*cos(theta)**19 - 4.42092752732811e+17*cos(theta)**17 + 1.01906126053665e+17*cos(theta)**15 - 1.70656191955898e+16*cos(theta)**13 + 2.01684590493334e+15*cos(theta)**11 - 160996407505564.0*cos(theta)**9 + 8117465924650.31*cos(theta)**7 - 231927597847.152*cos(theta)**5 + 3084143588.39297*cos(theta)**3 - 12094680.738796*cos(theta))*sin(4*phi)

#@torch.jit.script
def Yl39_m_minus_3(theta, phi):
    return 5.76968467048944e-5*(1.0 - cos(theta)**2)**1.5*(2.71469215174449e+15*cos(theta)**36 - 2.22111176051822e+16*cos(theta)**34 + 8.30695798433815e+16*cos(theta)**32 - 1.8813932238501e+17*cos(theta)**30 + 2.88171145202392e+17*cos(theta)**28 - 3.15735341700012e+17*cos(theta)**26 + 2.55258671772398e+17*cos(theta)**24 - 1.54838227272927e+17*cos(theta)**22 + 7.0967520833425e+16*cos(theta)**20 - 2.45607084851562e+16*cos(theta)**18 + 6.36913287835406e+15*cos(theta)**16 - 1.21897279968499e+15*cos(theta)**14 + 168070492077779.0*cos(theta)**12 - 16099640750556.4*cos(theta)**10 + 1014683240581.29*cos(theta)**8 - 38654599641.1919*cos(theta)**6 + 771035897.098243*cos(theta)**4 - 6047340.36939799*cos(theta)**2 + 7813.10125245218)*sin(3*phi)

#@torch.jit.script
def Yl39_m_minus_2(theta, phi):
    return 0.00227445624051009*(1.0 - cos(theta)**2)*(73370058155256.6*cos(theta)**37 - 634603360148063.0*cos(theta)**35 + 2.51725999525398e+15*cos(theta)**33 - 6.06901039951646e+15*cos(theta)**31 + 9.9369360414618e+15*cos(theta)**29 - 1.16939015444449e+16*cos(theta)**27 + 1.02103468708959e+16*cos(theta)**25 - 6.73209683795336e+15*cos(theta)**23 + 3.37940575397262e+15*cos(theta)**21 - 1.2926688676398e+15*cos(theta)**19 + 374654875197298.0*cos(theta)**17 - 81264853312332.5*cos(theta)**15 + 12928499390598.4*cos(theta)**13 - 1463603704596.04*cos(theta)**11 + 112742582286.81*cos(theta)**9 - 5522085663.02742*cos(theta)**7 + 154207179.419649*cos(theta)**5 - 2015780.12313266*cos(theta)**3 + 7813.10125245218*cos(theta))*sin(2*phi)

#@torch.jit.script
def Yl39_m_minus_1(theta, phi):
    return 0.0897762193123137*(1.0 - cos(theta)**2)**0.5*(1930791004085.7*cos(theta)**38 - 17627871115224.0*cos(theta)**36 + 74037058683940.7*cos(theta)**34 - 189656574984889.0*cos(theta)**32 + 331231201382060.0*cos(theta)**30 - 417639340873032.0*cos(theta)**28 + 392705648880612.0*cos(theta)**26 - 280504034914723.0*cos(theta)**24 + 153609352453301.0*cos(theta)**22 - 64633443381989.9*cos(theta)**20 + 20814159733183.2*cos(theta)**18 - 5079053332020.78*cos(theta)**16 + 923464242185.597*cos(theta)**14 - 121966975383.003*cos(theta)**12 + 11274258228.681*cos(theta)**10 - 690260707.878427*cos(theta)**8 + 25701196.5699414*cos(theta)**6 - 503945.030783166*cos(theta)**4 + 3906.55062622609*cos(theta)**2 - 5.01482750478317)*sin(phi)

#@torch.jit.script
def Yl39_m0(theta, phi):
    return 389968157002.95*cos(theta)**39 - 3752810445963.45*cos(theta)**37 + 16662478380077.7*cos(theta)**35 - 45270203818019.4*cos(theta)**33 + 84164322591247.4*cos(theta)**31 - 113438869579507.0*cos(theta)**29 + 114567614550448.0*cos(theta)**27 - 88380731224631.1*cos(theta)**25 + 52607578109899.4*cos(theta)**23 - 24243565139899.0*cos(theta)**21 + 8629065558269.14*cos(theta)**19 - 2353381515891.58*cos(theta)**17 + 484939221456.448*cos(theta)**15 - 73902203560.1263*cos(theta)**13 + 8073349968.75329*cos(theta)**11 - 604128228.954328*cos(theta)**9 + 28921032.2371753*cos(theta)**7 - 793910.688863635*cos(theta)**5 + 10257.2440421658*cos(theta)**3 - 39.501581677147*cos(theta)

#@torch.jit.script
def Yl39_m1(theta, phi):
    return 0.0897762193123137*(1.0 - cos(theta)**2)**0.5*(1930791004085.7*cos(theta)**38 - 17627871115224.0*cos(theta)**36 + 74037058683940.7*cos(theta)**34 - 189656574984889.0*cos(theta)**32 + 331231201382060.0*cos(theta)**30 - 417639340873032.0*cos(theta)**28 + 392705648880612.0*cos(theta)**26 - 280504034914723.0*cos(theta)**24 + 153609352453301.0*cos(theta)**22 - 64633443381989.9*cos(theta)**20 + 20814159733183.2*cos(theta)**18 - 5079053332020.78*cos(theta)**16 + 923464242185.597*cos(theta)**14 - 121966975383.003*cos(theta)**12 + 11274258228.681*cos(theta)**10 - 690260707.878427*cos(theta)**8 + 25701196.5699414*cos(theta)**6 - 503945.030783166*cos(theta)**4 + 3906.55062622609*cos(theta)**2 - 5.01482750478317)*cos(phi)

#@torch.jit.script
def Yl39_m2(theta, phi):
    return 0.00227445624051009*(1.0 - cos(theta)**2)*(73370058155256.6*cos(theta)**37 - 634603360148063.0*cos(theta)**35 + 2.51725999525398e+15*cos(theta)**33 - 6.06901039951646e+15*cos(theta)**31 + 9.9369360414618e+15*cos(theta)**29 - 1.16939015444449e+16*cos(theta)**27 + 1.02103468708959e+16*cos(theta)**25 - 6.73209683795336e+15*cos(theta)**23 + 3.37940575397262e+15*cos(theta)**21 - 1.2926688676398e+15*cos(theta)**19 + 374654875197298.0*cos(theta)**17 - 81264853312332.5*cos(theta)**15 + 12928499390598.4*cos(theta)**13 - 1463603704596.04*cos(theta)**11 + 112742582286.81*cos(theta)**9 - 5522085663.02742*cos(theta)**7 + 154207179.419649*cos(theta)**5 - 2015780.12313266*cos(theta)**3 + 7813.10125245218*cos(theta))*cos(2*phi)

#@torch.jit.script
def Yl39_m3(theta, phi):
    return 5.76968467048944e-5*(1.0 - cos(theta)**2)**1.5*(2.71469215174449e+15*cos(theta)**36 - 2.22111176051822e+16*cos(theta)**34 + 8.30695798433815e+16*cos(theta)**32 - 1.8813932238501e+17*cos(theta)**30 + 2.88171145202392e+17*cos(theta)**28 - 3.15735341700012e+17*cos(theta)**26 + 2.55258671772398e+17*cos(theta)**24 - 1.54838227272927e+17*cos(theta)**22 + 7.0967520833425e+16*cos(theta)**20 - 2.45607084851562e+16*cos(theta)**18 + 6.36913287835406e+15*cos(theta)**16 - 1.21897279968499e+15*cos(theta)**14 + 168070492077779.0*cos(theta)**12 - 16099640750556.4*cos(theta)**10 + 1014683240581.29*cos(theta)**8 - 38654599641.1919*cos(theta)**6 + 771035897.098243*cos(theta)**4 - 6047340.36939799*cos(theta)**2 + 7813.10125245218)*cos(3*phi)

#@torch.jit.script
def Yl39_m4(theta, phi):
    return 1.46644777253264e-6*(1.0 - cos(theta)**2)**2*(9.77289174628017e+16*cos(theta)**35 - 7.55177998576195e+17*cos(theta)**33 + 2.65822655498821e+18*cos(theta)**31 - 5.6441796715503e+18*cos(theta)**29 + 8.06879206566698e+18*cos(theta)**27 - 8.20911888420032e+18*cos(theta)**25 + 6.12620812253755e+18*cos(theta)**23 - 3.4064410000044e+18*cos(theta)**21 + 1.4193504166685e+18*cos(theta)**19 - 4.42092752732811e+17*cos(theta)**17 + 1.01906126053665e+17*cos(theta)**15 - 1.70656191955898e+16*cos(theta)**13 + 2.01684590493334e+15*cos(theta)**11 - 160996407505564.0*cos(theta)**9 + 8117465924650.31*cos(theta)**7 - 231927597847.152*cos(theta)**5 + 3084143588.39297*cos(theta)**3 - 12094680.738796*cos(theta))*cos(4*phi)

#@torch.jit.script
def Yl39_m5(theta, phi):
    return 3.73685494330611e-8*(1.0 - cos(theta)**2)**2.5*(3.42051211119806e+18*cos(theta)**34 - 2.49208739530144e+19*cos(theta)**32 + 8.24050232046344e+19*cos(theta)**30 - 1.63681210474959e+20*cos(theta)**28 + 2.17857385773009e+20*cos(theta)**26 - 2.05227972105008e+20*cos(theta)**24 + 1.40902786818364e+20*cos(theta)**22 - 7.15352610000924e+19*cos(theta)**20 + 2.69676579167015e+19*cos(theta)**18 - 7.51557679645779e+18*cos(theta)**16 + 1.52859189080497e+18*cos(theta)**14 - 2.21853049542668e+17*cos(theta)**12 + 2.21853049542668e+16*cos(theta)**10 - 1.44896766755008e+15*cos(theta)**8 + 56822261472552.1*cos(theta)**6 - 1159637989235.76*cos(theta)**4 + 9252430765.17892*cos(theta)**2 - 12094680.738796)*cos(5*phi)

#@torch.jit.script
def Yl39_m6(theta, phi):
    return 9.55345636639005e-10*(1.0 - cos(theta)**2)**3*(1.16297411780734e+20*cos(theta)**33 - 7.97467966496462e+20*cos(theta)**31 + 2.47215069613903e+21*cos(theta)**29 - 4.58307389329885e+21*cos(theta)**27 + 5.66429203009822e+21*cos(theta)**25 - 4.92547133052019e+21*cos(theta)**23 + 3.099861310004e+21*cos(theta)**21 - 1.43070522000185e+21*cos(theta)**19 + 4.85417842500627e+20*cos(theta)**17 - 1.20249228743325e+20*cos(theta)**15 + 2.14002864712696e+19*cos(theta)**13 - 2.66223659451201e+18*cos(theta)**11 + 2.21853049542668e+17*cos(theta)**9 - 1.15917413404006e+16*cos(theta)**7 + 340933568835313.0*cos(theta)**5 - 4638551956943.03*cos(theta)**3 + 18504861530.3578*cos(theta))*cos(6*phi)

#@torch.jit.script
def Yl39_m7(theta, phi):
    return 2.45202355926937e-11*(1.0 - cos(theta)**2)**3.5*(3.83781458876422e+21*cos(theta)**32 - 2.47215069613903e+22*cos(theta)**30 + 7.1692370188032e+22*cos(theta)**28 - 1.23742995119069e+23*cos(theta)**26 + 1.41607300752456e+23*cos(theta)**24 - 1.13285840601964e+23*cos(theta)**22 + 6.5097087510084e+22*cos(theta)**20 - 2.71833991800351e+22*cos(theta)**18 + 8.25210332251065e+21*cos(theta)**16 - 1.80373843114987e+21*cos(theta)**14 + 2.78203724126505e+20*cos(theta)**12 - 2.92846025396321e+19*cos(theta)**10 + 1.99667744588401e+18*cos(theta)**8 - 8.11421893828044e+16*cos(theta)**6 + 1.70466784417656e+15*cos(theta)**4 - 13915655870829.1*cos(theta)**2 + 18504861530.3578)*cos(7*phi)

#@torch.jit.script
def Yl39_m8(theta, phi):
    return 6.32267298839384e-13*(1.0 - cos(theta)**2)**4*(1.22810066840455e+23*cos(theta)**31 - 7.4164520884171e+23*cos(theta)**29 + 2.00738636526489e+24*cos(theta)**27 - 3.21731787309579e+24*cos(theta)**25 + 3.39857521805893e+24*cos(theta)**23 - 2.49228849324322e+24*cos(theta)**21 + 1.30194175020168e+24*cos(theta)**19 - 4.89301185240632e+23*cos(theta)**17 + 1.3203365316017e+23*cos(theta)**15 - 2.52523380360982e+22*cos(theta)**13 + 3.33844468951806e+21*cos(theta)**11 - 2.92846025396321e+20*cos(theta)**9 + 1.59734195670721e+19*cos(theta)**7 - 4.86853136296827e+17*cos(theta)**5 + 6.81867137670626e+15*cos(theta)**3 - 27831311741658.2*cos(theta))*cos(8*phi)

#@torch.jit.script
def Yl39_m9(theta, phi):
    return 1.63907661763532e-14*(1.0 - cos(theta)**2)**4.5*(3.80711207205411e+24*cos(theta)**30 - 2.15077110564096e+25*cos(theta)**28 + 5.41994318621522e+25*cos(theta)**26 - 8.04329468273948e+25*cos(theta)**24 + 7.81672300153555e+25*cos(theta)**22 - 5.23380583581076e+25*cos(theta)**20 + 2.47368932538319e+25*cos(theta)**18 - 8.31812014909074e+24*cos(theta)**16 + 1.98050479740256e+24*cos(theta)**14 - 3.28280394469276e+23*cos(theta)**12 + 3.67228915846987e+22*cos(theta)**10 - 2.63561422856689e+21*cos(theta)**8 + 1.11813936969505e+20*cos(theta)**6 - 2.43426568148413e+18*cos(theta)**4 + 2.04560141301188e+16*cos(theta)**2 - 27831311741658.2)*cos(9*phi)

#@torch.jit.script
def Yl39_m10(theta, phi):
    return 4.27504398551492e-16*(1.0 - cos(theta)**2)**5*(1.14213362161623e+26*cos(theta)**29 - 6.02215909579468e+26*cos(theta)**27 + 1.40918522841596e+27*cos(theta)**25 - 1.93039072385747e+27*cos(theta)**23 + 1.71967906033782e+27*cos(theta)**21 - 1.04676116716215e+27*cos(theta)**19 + 4.45264078568975e+26*cos(theta)**17 - 1.33089922385452e+26*cos(theta)**15 + 2.77270671636358e+25*cos(theta)**13 - 3.93936473363132e+24*cos(theta)**11 + 3.67228915846987e+23*cos(theta)**9 - 2.10849138285351e+22*cos(theta)**7 + 6.70883621817027e+20*cos(theta)**5 - 9.73706272593654e+18*cos(theta)**3 + 4.09120282602375e+16*cos(theta))*cos(10*phi)

#@torch.jit.script
def Yl39_m11(theta, phi):
    return 1.12268155211275e-17*(1.0 - cos(theta)**2)**5.5*(3.31218750268708e+27*cos(theta)**28 - 1.62598295586456e+28*cos(theta)**26 + 3.52296307103989e+28*cos(theta)**24 - 4.43989866487219e+28*cos(theta)**22 + 3.61132602670942e+28*cos(theta)**20 - 1.98884621760809e+28*cos(theta)**18 + 7.56948933567257e+27*cos(theta)**16 - 1.99634883578178e+27*cos(theta)**14 + 3.60451873127265e+26*cos(theta)**12 - 4.33330120699445e+25*cos(theta)**10 + 3.30506024262288e+24*cos(theta)**8 - 1.47594396799746e+23*cos(theta)**6 + 3.35441810908514e+21*cos(theta)**4 - 2.92111881778096e+19*cos(theta)**2 + 4.09120282602375e+16)*cos(11*phi)

#@torch.jit.script
def Yl39_m12(theta, phi):
    return 2.97093043392762e-19*(1.0 - cos(theta)**2)**6*(9.27412500752381e+28*cos(theta)**27 - 4.22755568524787e+29*cos(theta)**25 + 8.45511137049574e+29*cos(theta)**23 - 9.76777706271882e+29*cos(theta)**21 + 7.22265205341885e+29*cos(theta)**19 - 3.57992319169456e+29*cos(theta)**17 + 1.21111829370761e+29*cos(theta)**15 - 2.79488837009449e+28*cos(theta)**13 + 4.32542247752718e+27*cos(theta)**11 - 4.33330120699445e+26*cos(theta)**9 + 2.64404819409831e+25*cos(theta)**7 - 8.85566380798476e+23*cos(theta)**5 + 1.34176724363405e+22*cos(theta)**3 - 5.84223763556192e+19*cos(theta))*cos(12*phi)

#@torch.jit.script
def Yl39_m13(theta, phi):
    return 7.92882675780294e-21*(1.0 - cos(theta)**2)**6.5*(2.50401375203143e+30*cos(theta)**26 - 1.05688892131197e+31*cos(theta)**24 + 1.94467561521402e+31*cos(theta)**22 - 2.05123318317095e+31*cos(theta)**20 + 1.37230389014958e+31*cos(theta)**18 - 6.08586942588075e+30*cos(theta)**16 + 1.81667744056142e+30*cos(theta)**14 - 3.63335488112284e+29*cos(theta)**12 + 4.7579647252799e+28*cos(theta)**10 - 3.899971086295e+27*cos(theta)**8 + 1.85083373586881e+26*cos(theta)**6 - 4.42783190399238e+24*cos(theta)**4 + 4.02530173090216e+22*cos(theta)**2 - 5.84223763556192e+19)*cos(13*phi)

#@torch.jit.script
def Yl39_m14(theta, phi):
    return 2.13591674242462e-22*(1.0 - cos(theta)**2)**7*(6.51043575528172e+31*cos(theta)**25 - 2.53653341114872e+32*cos(theta)**23 + 4.27828635347084e+32*cos(theta)**21 - 4.1024663663419e+32*cos(theta)**19 + 2.47014700226925e+32*cos(theta)**17 - 9.7373910814092e+31*cos(theta)**15 + 2.54334841678598e+31*cos(theta)**13 - 4.3600258573474e+30*cos(theta)**11 + 4.7579647252799e+29*cos(theta)**9 - 3.119976869036e+28*cos(theta)**7 + 1.11050024152129e+27*cos(theta)**5 - 1.77113276159695e+25*cos(theta)**3 + 8.05060346180433e+22*cos(theta))*cos(14*phi)

#@torch.jit.script
def Yl39_m15(theta, phi):
    return 5.81322905778663e-24*(1.0 - cos(theta)**2)**7.5*(1.62760893882043e+33*cos(theta)**24 - 5.83402684564206e+33*cos(theta)**22 + 8.98440134228877e+33*cos(theta)**20 - 7.79468609604962e+33*cos(theta)**18 + 4.19924990385772e+33*cos(theta)**16 - 1.46060866221138e+33*cos(theta)**14 + 3.30635294182178e+32*cos(theta)**12 - 4.79602844308214e+31*cos(theta)**10 + 4.28216825275191e+30*cos(theta)**8 - 2.1839838083252e+29*cos(theta)**6 + 5.55250120760644e+27*cos(theta)**4 - 5.31339828479086e+25*cos(theta)**2 + 8.05060346180433e+22)*cos(15*phi)

#@torch.jit.script
def Yl39_m16(theta, phi):
    return 1.60003863775068e-25*(1.0 - cos(theta)**2)**8*(3.90626145316903e+34*cos(theta)**23 - 1.28348590604125e+35*cos(theta)**21 + 1.79688026845775e+35*cos(theta)**19 - 1.40304349728893e+35*cos(theta)**17 + 6.71879984617235e+34*cos(theta)**15 - 2.04485212709593e+34*cos(theta)**13 + 3.96762353018614e+33*cos(theta)**11 - 4.79602844308214e+32*cos(theta)**9 + 3.42573460220153e+31*cos(theta)**7 - 1.31039028499512e+30*cos(theta)**5 + 2.22100048304258e+28*cos(theta)**3 - 1.06267965695817e+26*cos(theta))*cos(16*phi)

#@torch.jit.script
def Yl39_m17(theta, phi):
    return 4.45833336048602e-27*(1.0 - cos(theta)**2)**8.5*(8.98440134228877e+35*cos(theta)**22 - 2.69532040268663e+36*cos(theta)**20 + 3.41407251006973e+36*cos(theta)**18 - 2.38517394539118e+36*cos(theta)**16 + 1.00781997692585e+36*cos(theta)**14 - 2.65830776522471e+35*cos(theta)**12 + 4.36438588320475e+34*cos(theta)**10 - 4.31642559877393e+33*cos(theta)**8 + 2.39801422154107e+32*cos(theta)**6 - 6.5519514249756e+30*cos(theta)**4 + 6.66300144912773e+28*cos(theta)**2 - 1.06267965695817e+26)*cos(17*phi)

#@torch.jit.script
def Yl39_m18(theta, phi):
    return 1.25899431882528e-28*(1.0 - cos(theta)**2)**9*(1.97656829530353e+37*cos(theta)**21 - 5.39064080537326e+37*cos(theta)**19 + 6.14533051812552e+37*cos(theta)**17 - 3.81627831262589e+37*cos(theta)**15 + 1.41094796769619e+37*cos(theta)**13 - 3.18996931826965e+36*cos(theta)**11 + 4.36438588320475e+35*cos(theta)**9 - 3.45314047901914e+34*cos(theta)**7 + 1.43880853292464e+33*cos(theta)**5 - 2.62078056999024e+31*cos(theta)**3 + 1.33260028982555e+29*cos(theta))*cos(18*phi)

#@torch.jit.script
def Yl39_m19(theta, phi):
    return 3.60744838710617e-30*(1.0 - cos(theta)**2)**9.5*(4.15079342013741e+38*cos(theta)**20 - 1.02422175302092e+39*cos(theta)**18 + 1.04470618808134e+39*cos(theta)**16 - 5.72441746893884e+38*cos(theta)**14 + 1.83423235800505e+38*cos(theta)**12 - 3.50896625009662e+37*cos(theta)**10 + 3.92794729488427e+36*cos(theta)**8 - 2.4171983353134e+35*cos(theta)**6 + 7.19404266462321e+33*cos(theta)**4 - 7.86234170997073e+31*cos(theta)**2 + 1.33260028982555e+29)*cos(19*phi)

#@torch.jit.script
def Yl39_m20(theta, phi):
    return 1.05016882684848e-31*(1.0 - cos(theta)**2)**10*(8.30158684027482e+39*cos(theta)**19 - 1.84359915543766e+40*cos(theta)**17 + 1.67152990093014e+40*cos(theta)**15 - 8.01418445651438e+39*cos(theta)**13 + 2.20107882960606e+39*cos(theta)**11 - 3.50896625009662e+38*cos(theta)**9 + 3.14235783590742e+37*cos(theta)**7 - 1.45031900118804e+36*cos(theta)**5 + 2.87761706584929e+34*cos(theta)**3 - 1.57246834199415e+32*cos(theta))*cos(20*phi)

#@torch.jit.script
def Yl39_m21(theta, phi):
    return 3.1103316302064e-33*(1.0 - cos(theta)**2)**10.5*(1.57730149965222e+41*cos(theta)**18 - 3.13411856424401e+41*cos(theta)**16 + 2.50729485139521e+41*cos(theta)**14 - 1.04184397934687e+41*cos(theta)**12 + 2.42118671256667e+40*cos(theta)**10 - 3.15806962508696e+39*cos(theta)**8 + 2.19965048513519e+38*cos(theta)**6 - 7.2515950059402e+36*cos(theta)**4 + 8.63285119754786e+34*cos(theta)**2 - 1.57246834199415e+32)*cos(21*phi)

#@torch.jit.script
def Yl39_m22(theta, phi):
    return 9.38653981934599e-35*(1.0 - cos(theta)**2)**11*(2.83914269937399e+42*cos(theta)**17 - 5.01458970279042e+42*cos(theta)**15 + 3.5102127919533e+42*cos(theta)**13 - 1.25021277521624e+42*cos(theta)**11 + 2.42118671256667e+41*cos(theta)**9 - 2.52645570006957e+40*cos(theta)**7 + 1.31979029108112e+39*cos(theta)**5 - 2.90063800237608e+37*cos(theta)**3 + 1.72657023950957e+35*cos(theta))*cos(22*phi)

#@torch.jit.script
def Yl39_m23(theta, phi):
    return 2.89124717480577e-36*(1.0 - cos(theta)**2)**11.5*(4.82654258893578e+43*cos(theta)**16 - 7.52188455418563e+43*cos(theta)**14 + 4.56327662953929e+43*cos(theta)**12 - 1.37523405273787e+43*cos(theta)**10 + 2.17906804131e+42*cos(theta)**8 - 1.7685189900487e+41*cos(theta)**6 + 6.59895145540558e+39*cos(theta)**4 - 8.70191400712824e+37*cos(theta)**2 + 1.72657023950957e+35)*cos(23*phi)

#@torch.jit.script
def Yl39_m24(theta, phi):
    return 9.10657262304068e-38*(1.0 - cos(theta)**2)**12*(7.72246814229725e+44*cos(theta)**15 - 1.05306383758599e+45*cos(theta)**13 + 5.47593195544714e+44*cos(theta)**11 - 1.37523405273787e+44*cos(theta)**9 + 1.743254433048e+43*cos(theta)**7 - 1.06111139402922e+42*cos(theta)**5 + 2.63958058216223e+40*cos(theta)**3 - 1.74038280142565e+38*cos(theta))*cos(24*phi)

#@torch.jit.script
def Yl39_m25(theta, phi):
    return 2.93913367583875e-39*(1.0 - cos(theta)**2)**12.5*(1.15837022134459e+46*cos(theta)**14 - 1.36898298886179e+46*cos(theta)**12 + 6.02352515099186e+45*cos(theta)**10 - 1.23771064746408e+45*cos(theta)**8 + 1.2202781031336e+44*cos(theta)**6 - 5.30555697014609e+42*cos(theta)**4 + 7.9187417464867e+40*cos(theta)**2 - 1.74038280142565e+38)*cos(25*phi)

#@torch.jit.script
def Yl39_m26(theta, phi):
    return 9.74313326210721e-41*(1.0 - cos(theta)**2)**13*(1.62171830988242e+47*cos(theta)**13 - 1.64277958663414e+47*cos(theta)**11 + 6.02352515099186e+46*cos(theta)**9 - 9.90168517971264e+45*cos(theta)**7 + 7.3216686188016e+44*cos(theta)**5 - 2.12222278805844e+43*cos(theta)**3 + 1.58374834929734e+41*cos(theta))*cos(26*phi)

#@torch.jit.script
def Yl39_m27(theta, phi):
    return 3.326250851581e-42*(1.0 - cos(theta)**2)**13.5*(2.10823380284715e+48*cos(theta)**12 - 1.80705754529756e+48*cos(theta)**10 + 5.42117263589267e+47*cos(theta)**8 - 6.93117962579885e+46*cos(theta)**6 + 3.6608343094008e+45*cos(theta)**4 - 6.3666683641753e+43*cos(theta)**2 + 1.58374834929734e+41)*cos(27*phi)

#@torch.jit.script
def Yl39_m28(theta, phi):
    return 1.1730782277043e-43*(1.0 - cos(theta)**2)**14*(2.52988056341658e+49*cos(theta)**11 - 1.80705754529756e+49*cos(theta)**9 + 4.33693810871414e+48*cos(theta)**7 - 4.15870777547931e+47*cos(theta)**5 + 1.46433372376032e+46*cos(theta)**3 - 1.27333367283506e+44*cos(theta))*cos(28*phi)

#@torch.jit.script
def Yl39_m29(theta, phi):
    return 4.28919879632039e-45*(1.0 - cos(theta)**2)**14.5*(2.78286861975824e+50*cos(theta)**10 - 1.6263517907678e+50*cos(theta)**8 + 3.0358566760999e+49*cos(theta)**6 - 2.07935388773965e+48*cos(theta)**4 + 4.39300117128096e+46*cos(theta)**2 - 1.27333367283506e+44)*cos(29*phi)

#@torch.jit.script
def Yl39_m30(theta, phi):
    return 1.63287007543161e-46*(1.0 - cos(theta)**2)**15*(2.78286861975824e+51*cos(theta)**9 - 1.30108143261424e+51*cos(theta)**7 + 1.82151400565994e+50*cos(theta)**5 - 8.31741555095862e+48*cos(theta)**3 + 8.78600234256192e+46*cos(theta))*cos(30*phi)

#@torch.jit.script
def Yl39_m31(theta, phi):
    return 6.50551009827291e-48*(1.0 - cos(theta)**2)**15.5*(2.50458175778241e+52*cos(theta)**8 - 9.10757002829969e+51*cos(theta)**6 + 9.10757002829969e+50*cos(theta)**4 - 2.49522466528759e+49*cos(theta)**2 + 8.78600234256192e+46)*cos(31*phi)

#@torch.jit.script
def Yl39_m32(theta, phi):
    return 2.72965140034074e-49*(1.0 - cos(theta)**2)**16*(2.00366540622593e+53*cos(theta)**7 - 5.46454201697981e+52*cos(theta)**5 + 3.64302801131987e+51*cos(theta)**3 - 4.99044933057517e+49*cos(theta))*cos(32*phi)

#@torch.jit.script
def Yl39_m33(theta, phi):
    return 1.21588337207176e-50*(1.0 - cos(theta)**2)**16.5*(1.40256578435815e+54*cos(theta)**6 - 2.73227100848991e+53*cos(theta)**4 + 1.09290840339596e+52*cos(theta)**2 - 4.99044933057517e+49)*cos(33*phi)

#@torch.jit.script
def Yl39_m34(theta, phi):
    return 5.80971547822379e-52*(1.0 - cos(theta)**2)**17*(8.41539470614891e+54*cos(theta)**5 - 1.09290840339596e+54*cos(theta)**3 + 2.18581680679192e+52*cos(theta))*cos(34*phi)

#@torch.jit.script
def Yl39_m35(theta, phi):
    return 3.02032725709922e-53*(1.0 - cos(theta)**2)**17.5*(4.20769735307446e+55*cos(theta)**4 - 3.27872521018789e+54*cos(theta)**2 + 2.18581680679192e+52)*cos(35*phi)

#@torch.jit.script
def Yl39_m36(theta, phi):
    return 1.743786754927e-54*(1.0 - cos(theta)**2)**18*(1.68307894122978e+56*cos(theta)**3 - 6.55745042037577e+54*cos(theta))*cos(36*phi)

#@torch.jit.script
def Yl39_m37(theta, phi):
    return 1.15485099036113e-55*(1.0 - cos(theta)**2)**18.5*(5.04923682368935e+56*cos(theta)**2 - 6.55745042037577e+54)*cos(37*phi)

#@torch.jit.script
def Yl39_m38(theta, phi):
    return 9.39769459334552*(1.0 - cos(theta)**2)**19*cos(38*phi)*cos(theta)

#@torch.jit.script
def Yl39_m39(theta, phi):
    return 1.064079376195*(1.0 - cos(theta)**2)**19.5*cos(39*phi)

