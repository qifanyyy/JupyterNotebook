'''
Copyright (C) <2015>  <Jorge Silva> <up201007483@alunos.dcc.fc.up.pt>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

This work was partially supported by national funds through project VOCE 
(PTDC/EEA-ELC/121018/2010), and in the scope of R&D Unit UID/EEA/50008/2013, 
funded by FCT/MEC through national funds and when applicable cofunded
by FEDER/PT2020 partnership agreement.
'''

class data_instance:
    def __init__(self, i, e, st, d, vals, s):
        self.id = i
        self.event = e
        self.start_time = st
        self.duration = d
        self.values = vals
        self.stress = s
        
        
class ML_set:
    def __init__(self, f_vals, f_preds, f_numbers):
        self.fts_values = f_vals
        self.fts_pred = f_preds
        self.fts_numbers = f_numbers
        
        
class ML_subset:
    def __init__(self, fts, accs):
        self.features = fts
        self.parents_accuracy = accs