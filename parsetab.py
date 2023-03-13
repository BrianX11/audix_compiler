
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'startFRACCION ID INSTRUMENTO LCURLY NOTA PATRON PISTA PLAY RCURLY VOZ ignore ignore_COMMENTfuncion : PLAY IDpatron : PATRON ID LCURLY patron_bloque RCURLYpatron_bloque : voz\n\t| patron_bloque vozpista : PISTA ID LCURLY pista_bloque RCURLYpista_bloque : funcion\n\t| pista_bloque funcionprogram : pista program\n\t| patron program\n\t| pista\n\t| patronstart : programvoz : VOZ ID LCURLY voz_bloque RCURLYvoz_bloque : NOTA FRACCION\n\t| voz_bloque NOTA FRACCION'
    
_lr_action_items = {'PISTA':([0,3,4,19,22,],[5,5,5,-5,-2,]),'PATRON':([0,3,4,19,22,],[6,6,6,-5,-2,]),'$end':([1,2,3,4,7,8,19,22,],[0,-12,-10,-11,-8,-9,-5,-2,]),'ID':([5,6,15,18,],[9,10,21,24,]),'LCURLY':([9,10,24,],[11,12,25,]),'PLAY':([11,13,14,20,21,],[15,15,-6,-7,-1,]),'VOZ':([12,16,17,23,28,],[18,18,-3,-4,-13,]),'RCURLY':([13,14,16,17,20,21,23,26,28,30,31,],[19,-6,22,-3,-7,-1,-4,28,-13,-14,-15,]),'NOTA':([25,26,30,31,],[27,29,-14,-15,]),'FRACCION':([27,29,],[30,31,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'program':([0,3,4,],[2,7,8,]),'pista':([0,3,4,],[3,3,3,]),'patron':([0,3,4,],[4,4,4,]),'pista_bloque':([11,],[13,]),'funcion':([11,13,],[14,20,]),'patron_bloque':([12,],[16,]),'voz':([12,16,],[17,23,]),'voz_bloque':([25,],[26,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('funcion -> PLAY ID','funcion',2,'p_funcion','audix_yacc.py',2),
  ('patron -> PATRON ID LCURLY patron_bloque RCURLY','patron',5,'p_patron','audix_yacc.py',2),
  ('patron_bloque -> voz','patron_bloque',1,'p_patron_bloque','audix_yacc.py',2),
  ('patron_bloque -> patron_bloque voz','patron_bloque',2,'p_patron_bloque','audix_yacc.py',3),
  ('pista -> PISTA ID LCURLY pista_bloque RCURLY','pista',5,'p_pista','audix_yacc.py',2),
  ('pista_bloque -> funcion','pista_bloque',1,'p_pista_bloque','audix_yacc.py',2),
  ('pista_bloque -> pista_bloque funcion','pista_bloque',2,'p_pista_bloque','audix_yacc.py',3),
  ('program -> pista program','program',2,'p_program','audix_yacc.py',2),
  ('program -> patron program','program',2,'p_program','audix_yacc.py',3),
  ('program -> pista','program',1,'p_program','audix_yacc.py',4),
  ('program -> patron','program',1,'p_program','audix_yacc.py',5),
  ('start -> program','start',1,'p_start','audix_yacc.py',2),
  ('voz -> VOZ ID LCURLY voz_bloque RCURLY','voz',5,'p_voz','audix_yacc.py',2),
  ('voz_bloque -> NOTA FRACCION','voz_bloque',2,'p_voz_bloque','audix_yacc.py',2),
  ('voz_bloque -> voz_bloque NOTA FRACCION','voz_bloque',3,'p_voz_bloque','audix_yacc.py',3),
]
