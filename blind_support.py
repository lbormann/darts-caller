"""
Blind Support Module for Darts Caller
Provides audio feedback for visually impaired players
"""

class BlindSupport:
    """
    Handles blind support calls for different game modes.
    Announces targets and dart positions to assist visually impaired players.
    """
    
    def __init__(self, sound_effect_callback, enabled=False):
        """
        Initialize BlindSupport
        
        Args:
            sound_effect_callback: Function to play sound effects
            enabled: Whether blind support is enabled
        """
        self.play_sound = sound_effect_callback
        self.enabled = enabled
        self.last_announced_target = None
        
    def set_enabled(self, enabled):
        """Enable or disable blind support"""
        self.enabled = enabled
        
    def announce_turn_start(self, game_mode, game_data):
        """
        Announce target at the start of a player's turn
        
        Args:
            game_mode: Current game mode (X01, ATC, RTW, etc.)
            game_data: Game state data from websocket
        """
        if not self.enabled:
            return
            
        if game_mode == 'ATC':
            self._announce_atc_target(game_data)
        elif game_mode == 'RTW':
            self._announce_rtw_target(game_data)
        elif game_mode == 'Bermuda':
            self._announce_bermuda_target(game_data)
        elif game_mode == 'Shanghai':
            self._announce_shanghai_target(game_data)
            
    def announce_dart_result(self, game_mode, throw_data):
        """
        Announce where a dart landed
        
        Args:
            game_mode: Current game mode
            throw_data: Dart throw data from websocket
        """
        if not self.enabled:
            return
            
        self._announce_dart_position(throw_data)
        
    def _announce_atc_target(self, game_data):
        """Announce current target for ATC mode"""
        try:
            current_player_index = game_data['player']
            current_targets_player = game_data['state']['currentTargets'][current_player_index]
            current_target = game_data['state']['targets'][current_player_index][int(current_targets_player)]
            
            target_number = str(current_target['number'])
            target_bed = current_target['bed']
            
            # Announce "target is"
            if self.play_sound('bs_target_is', wait_for_last=True):
                # Announce bed type if not "Full"
                if target_bed != 'Full':
                    bed_key = self._get_bed_sound_key(target_bed)
                    if bed_key:
                        self.play_sound(bed_key, wait_for_last=True)
                
                # Announce number
                self.play_sound(target_number, wait_for_last=True)
                
        except Exception as e:
            pass
                
    def _announce_rtw_target(self, game_data):
        """Announce current target for RTW mode"""
        try:
            round_num = game_data['round']
            order = game_data['settings']['order']
            
            if order == '1-20-Bull':
                target = round_num
            elif order == '20-1-Bull':
                target = 21 - round_num
            else:
                return  # Random order, target varies
                
            if target == 0 or target == 21:
                target = 25
            
            # Announce "target is"
            if self.play_sound('bs_target_is', wait_for_last=True):
                self.play_sound(str(target), wait_for_last=True)
                
        except Exception as e:
            pass
                
    def _announce_bermuda_target(self, game_data):
        """Announce current target for Bermuda mode"""
        try:
            # Bermuda rounds mapping
            BERMUDA_ROUNDS = {
                1: '12',
                2: '13',
                3: '14',
                4: 'D',
                5: '15',
                6: '16',
                7: '17',
                8: 'T',
                9: '18',
                10: '19',
                11: '20',
                12: '25',
                13: '50'
            }
            
            round_num = game_data['round']
            target = BERMUDA_ROUNDS.get(round_num)
            
            if not target:
                return
            
            # Announce "target is"
            if self.play_sound('bs_target_is', wait_for_last=True):
                # Handle special targets
                if target == 'D':
                    self.play_sound('bs_any_double', wait_for_last=True)
                elif target == 'T':
                    self.play_sound('bs_any_triple', wait_for_last=True)
                elif target == '50':
                    self.play_sound('bullseye', wait_for_last=True)
                elif target == '25':
                    self.play_sound('bull', wait_for_last=True)
                else:
                    self.play_sound(target, wait_for_last=True)
                    
        except Exception as e:
            pass
                
    def _announce_shanghai_target(self, game_data):
        """Announce current target for Shanghai mode"""
        try:
            round_num = game_data['round']
            
            # Announce "target is"
            if self.play_sound('bs_target_is', wait_for_last=True):
                self.play_sound(str(round_num), wait_for_last=True)
                
        except Exception as e:
            pass
                
    def _announce_dart_position(self, throw_data):
        """Announce where a dart landed"""
        try:
            segment = throw_data['segment']
            bed = segment['bed']
            number = segment['number']
            number_str = str(number)
            
            # Special handling for bull
            if number == 25:
                if bed == 'Double':
                    self.play_sound('bullseye', wait_for_last=True)
                else:
                    self.play_sound('bull', wait_for_last=True)
                return
            
            # Handle different bed types
            if bed == 'Triple':
                # Try t20, t19, etc.
                if not self.play_sound('t' + number_str, wait_for_last=True):
                    # Fallback to "triple" + number
                    if self.play_sound('bs_triple', wait_for_last=True):
                        self.play_sound(number_str, wait_for_last=True)
                    else:
                        self.play_sound(number_str, wait_for_last=True)
                        
            elif bed == 'Double':
                # Try d20, d19, etc.
                if not self.play_sound('d' + number_str, wait_for_last=True):
                    # Fallback to "double" + number
                    if self.play_sound('bs_double', wait_for_last=True):
                        self.play_sound(number_str, wait_for_last=True)
                    else:
                        self.play_sound(number_str, wait_for_last=True)
                        
            elif bed == 'Outside':
                # Try m20, m19, etc.
                if not self.play_sound('m' + number_str, wait_for_last=True):
                    # Fallback to "outside" + number
                    if self.play_sound('bs_outside', wait_for_last=True):
                        self.play_sound(number_str, wait_for_last=True)
                    else:
                        self.play_sound(number_str, wait_for_last=True)
                        
            elif bed == 'SingleOuter' or bed == 'Outer Single':
                # Only announce number for outer single
                self.play_sound(number_str, wait_for_last=True)
                
            elif bed == 'SingleInner' or bed == 'Inner Single':
                # Announce "single inner" + number
                if self.play_sound('bs_single_inner', wait_for_last=True):
                    self.play_sound(number_str, wait_for_last=True)
                else:
                    self.play_sound(number_str, wait_for_last=True)
                    
            elif bed == 'Single':
                # Generic single - just announce number
                self.play_sound(number_str, wait_for_last=True)
            else:
                # Fallback for any other bed type
                self.play_sound(number_str, wait_for_last=True)
                
        except Exception as e:
            pass
                
    def _get_bed_sound_key(self, bed):
        """
        Get sound key for bed type
        
        Returns sound keys like: bs_single, bs_double, bs_triple, bs_outside
        """
        bed_mapping = {
            'Single': 'bs_single',
            'SingleInner': 'bs_single_inner',
            'SingleOuter': 'bs_single_outer',
            'Double': 'bs_double',
            'Triple': 'bs_triple',
            'Outside': 'bs_outside',
            'Inner Single': 'bs_single_inner',
            'Outer Single': 'bs_single_outer',
            'Full': None  # No bed announcement for full field
        }
        return bed_mapping.get(bed)
        
    def reset_target(self):
        """Reset last announced target"""
        self.last_announced_target = None
