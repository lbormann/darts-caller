"""
WebSocket and API Message Logger with dual output
Creates two log files:
- messages_TIMESTAMP.log: Summary with extracted info only
- messages_TIMESTAMP_full.log: Complete JSON messages
"""

import json
import os
from datetime import datetime
from threading import Lock
import traceback


class MessageLogger:
    def __init__(self, enabled=False, log_dir="logs"):
        """
        Initialize the message logger
        
        Args:
            enabled: Whether logging is enabled
            log_dir: Directory to store log files
        """
        self.enabled = enabled
        self.log_dir = log_dir
        self.log_file = None
        self.log_file_full = None
        self.write_lock = Lock()
        self.message_counter = 0
        
        if self.enabled:
            self._create_log_files()
    
    def _create_log_files(self):
        """Create log directory and both log files with timestamp"""
        try:
            # Create log directory if it doesn't exist
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            
            # Create log files with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = os.path.join(self.log_dir, f"messages_{timestamp}.log")
            self.log_file_full = os.path.join(self.log_dir, f"messages_{timestamp}_full.log")
            
            # Write headers to both files
            header = "=" * 100 + "\n"
            header += f"Message Logger started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += "=" * 100 + "\n\n"
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write("This file contains SUMMARY information only (no JSON).\n")
                f.write("For full JSON messages, see the corresponding _full.log file.\n")
                f.write("=" * 100 + "\n\n")
            
            with open(self.log_file_full, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write("This file contains FULL JSON messages.\n")
                f.write("=" * 100 + "\n\n")
            
            print(f"Message logging enabled:")
            print(f"  Summary: {self.log_file}")
            print(f"  Full:    {self.log_file_full}")
        except Exception as e:
            print(f"Failed to create log files: {e}")
            self.enabled = False
    
    def _write_to_both_logs(self, summary_content, full_content):
        """Thread-safe write to both log files"""
        if not self.enabled or not self.log_file:
            return
        
        with self.write_lock:
            try:
                # Write summary to main log
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(summary_content)
                    f.flush()
                
                # Write full version to full log
                with open(self.log_file_full, 'a', encoding='utf-8') as f:
                    f.write(full_content)
                    f.flush()
            except Exception as e:
                print(f"Error writing to message logs: {e}")
    
    def log_websocket_message(self, message, direction="INCOMING", channel=None, event=None, additional_info=None):
        """
        Log a WebSocket message to both files
        
        Args:
            message: The message (can be dict or string)
            direction: INCOMING or OUTGOING
            channel: WebSocket channel
            event: Event type
            additional_info: Dictionary with additional context
        """
        if not self.enabled:
            return
        
        try:
            self.message_counter += 1
            msg_id = self.message_counter
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            # Parse message if it's a string
            if isinstance(message, str):
                try:
                    message_dict = json.loads(message)
                except:
                    message_dict = None
            else:
                message_dict = message
            
            # Extract additional information from message content
            extracted_info = self._extract_message_info(message_dict, channel, event)
            
            # Merge with provided additional_info
            if additional_info:
                extracted_info.update(additional_info)
            
            # Build SUMMARY content (no JSON)
            separator = "─" * 100
            summary = f"\n{separator}\n"
            summary += f"[{timestamp}] MSG #{msg_id} - WEBSOCKET {direction}\n"
            summary += f"{separator}\n"
            
            if channel:
                summary += f"Channel: {channel}\n"
            
            # Show topic for subscribe/unsubscribe messages
            if message_dict and isinstance(message_dict, dict):
                msg_type = message_dict.get('type', '')
                topic = message_dict.get('topic', '')
                if msg_type in ['subscribe', 'unsubscribe'] and topic:
                    summary += f"Topic: {topic}\n"
            
            if event:
                summary += f"Event: {event}\n"
            
            if extracted_info:
                summary += "Extracted Info:\n"
                for key, value in extracted_info.items():
                    summary += f"  {key}: {value}\n"
            
            # Build FULL content (with JSON)
            full = f"\n{separator}\n"
            full += f"[{timestamp}] MSG #{msg_id} - WEBSOCKET {direction}\n"
            full += f"{separator}\n"
            
            if channel:
                full += f"Channel: {channel}\n"
            
            # Show topic for subscribe/unsubscribe messages
            if message_dict and isinstance(message_dict, dict):
                msg_type = message_dict.get('type', '')
                topic = message_dict.get('topic', '')
                if msg_type in ['subscribe', 'unsubscribe'] and topic:
                    full += f"Topic: {topic}\n"
            
            if event:
                full += f"Event: {event}\n"
            
            if extracted_info:
                full += "Extracted Info:\n"
                for key, value in extracted_info.items():
                    full += f"  {key}: {value}\n"
            
            full += "\nFull Message JSON:\n"
            
            # Format message for full log
            if isinstance(message, dict):
                full += json.dumps(message, indent=2, ensure_ascii=False)
            elif isinstance(message, str):
                try:
                    msg_dict = json.loads(message)
                    full += json.dumps(msg_dict, indent=2, ensure_ascii=False)
                except:
                    full += message
            else:
                full += str(message)
            
            full += "\n"
            
            self._write_to_both_logs(summary, full)
        
        except Exception as e:
            self.log_error(f"Failed to log WebSocket message: {e}\n{traceback.format_exc()}")
    
    def log_api_request(self, method, url, headers=None, params=None, data=None, response=None):
        """
        Log an API request and response to both files
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            headers: Request headers
            params: Query parameters
            data: Request body
            response: Response object or dict
        """
        if not self.enabled:
            return
        
        try:
            self.message_counter += 1
            msg_id = self.message_counter
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            separator = "─" * 100
            
            # Build SUMMARY content
            summary = f"\n{separator}\n"
            summary += f"[{timestamp}] MSG #{msg_id} - API REQUEST {method}\n"
            summary += f"{separator}\n"
            summary += f"URL: {url}\n"
            
            if response:
                if hasattr(response, 'status_code'):
                    summary += f"Status: {response.status_code}\n"
                elif isinstance(response, dict) and 'status' in response:
                    summary += f"Status: {response['status']}\n"
            
            # Build FULL content
            full = f"\n{separator}\n"
            full += f"[{timestamp}] MSG #{msg_id} - API REQUEST {method}\n"
            full += f"{separator}\n"
            full += f"URL: {url}\n"
            
            if headers:
                full += f"\nHeaders:\n{json.dumps(dict(headers) if not isinstance(headers, dict) else headers, indent=2, ensure_ascii=False)}\n"
            
            if params:
                full += f"\nParameters:\n{json.dumps(params, indent=2, ensure_ascii=False)}\n"
            
            if data:
                full += f"\nRequest Data:\n"
                if isinstance(data, (dict, list)):
                    full += json.dumps(data, indent=2, ensure_ascii=False)
                else:
                    full += str(data)
                full += "\n"
            
            if response:
                full += f"\nResponse:\n"
                if hasattr(response, 'json'):
                    try:
                        full += json.dumps(response.json(), indent=2, ensure_ascii=False)
                    except:
                        full += str(response.text if hasattr(response, 'text') else response)
                elif isinstance(response, (dict, list)):
                    full += json.dumps(response, indent=2, ensure_ascii=False)
                else:
                    full += str(response)
                full += "\n"
            
            self._write_to_both_logs(summary, full)
        
        except Exception as e:
            self.log_error(f"Failed to log API request: {e}\n{traceback.format_exc()}")
    
    def log_event(self, event_name, details=None):
        """
        Log a custom event to both files
        
        Args:
            event_name: Name of the event
            details: Additional details (dict or string)
        """
        if not self.enabled:
            return
        
        try:
            self.message_counter += 1
            msg_id = self.message_counter
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            separator = "─" * 100
            
            # SUMMARY
            summary = f"\n{separator}\n"
            summary += f"[{timestamp}] MSG #{msg_id} - EVENT: {event_name}\n"
            summary += f"{separator}\n"
            
            if details and isinstance(details, str):
                summary += f"{details}\n"
            elif details and isinstance(details, dict):
                # Extract key info for summary
                for key, value in details.items():
                    summary += f"  {key}: {value}\n"
            
            # FULL
            full = f"\n{separator}\n"
            full += f"[{timestamp}] MSG #{msg_id} - EVENT: {event_name}\n"
            full += f"{separator}\n"
            
            if details:
                if isinstance(details, dict):
                    full += json.dumps(details, indent=2, ensure_ascii=False) + "\n"
                else:
                    full += str(details) + "\n"
            
            self._write_to_both_logs(summary, full)
        
        except Exception as e:
            self.log_error(f"Failed to log event: {e}\n{traceback.format_exc()}")
    
    def log_error(self, error_message):
        """
        Log an error to both files
        
        Args:
            error_message: Error message or exception
        """
        if not self.enabled:
            return
        
        try:
            self.message_counter += 1
            msg_id = self.message_counter
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            separator = "─" * 100
            content = f"\n{separator}\n"
            content += f"[{timestamp}] MSG #{msg_id} - ERROR\n"
            content += f"{separator}\n"
            content += f"{error_message}\n"
            
            # Errors go to both files identically
            self._write_to_both_logs(content, content)
        
        except Exception as e:
            print(f"Failed to log error: {e}")
    
    def _extract_message_info(self, message_dict, channel=None, event=None):
        """
        Extract useful information from message data with extended details
        
        Args:
            message_dict: The message dictionary
            channel: Channel name
            event: Event name
            
        Returns:
            dict: Extracted information
        """
        info = {}
        
        try:
            if not isinstance(message_dict, dict):
                return info
            
            # Use channel from message if not provided
            if not channel and 'channel' in message_dict:
                channel = message_dict['channel']
            
            # Get the data payload
            data = message_dict.get('data', {})
            
            # === LOBBY & MATCH LIFECYCLE EVENTS ===
            # Detect important lifecycle events for easy searching
            
            # 1. Lobby Enter (User creates/joins a lobby)
            if channel == 'autodarts.users' and data.get('event') == 'lobby-enter':
                body = data.get('body', {})
                if body.get('type') == 'lobby':
                    info['🎯 LIFECYCLE'] = '🔵 LOBBY OPENED'
                    info['lobby_id'] = body.get('id', 'unknown')
            
            # 2. Lobby Start (Match configuration ready, waiting for board start)
            elif channel == 'autodarts.lobbies' and data.get('event') == 'start':
                info['🎯 LIFECYCLE'] = '🟡 LOBBY STARTED (waiting for board)'
                info['match_id'] = data.get('id', 'unknown')
            
            # 3. Match Start on Board (Game actually begins)
            elif channel == 'autodarts.boards':
                topic = message_dict.get('topic', '')
                event_type = data.get('event', '')
                
                if '.matches' in topic and event_type == 'start':
                    info['🎯 LIFECYCLE'] = '🟢 MATCH STARTED'
                    info['match_id'] = data.get('id', 'unknown')
                elif '.events' in topic and event_type == 'Started':
                    info['🎯 LIFECYCLE'] = '✅ GAME ACTIVE (first throw ready)'
                
                # 4. Match Finish
                elif '.matches' in topic and event_type == 'finish':
                    info['🎯 LIFECYCLE'] = '🔴 MATCH FINISHED'
                    info['match_id'] = data.get('id', 'unknown')
            
            # Match messages
            if channel == 'autodarts.matches':
                info['match_active'] = True
                
                # Match ID
                if 'id' in data:
                    info['current_match'] = data['id']
                
                # Game finished status
                if 'finished' in data:
                    info['match_finished'] = data['finished']
                if 'gameFinished' in data:
                    info['game_finished'] = data['gameFinished']
                if 'winner' in data and data['winner'] >= 0:
                    info['winner_index'] = data['winner']
                
                # Game variant and settings
                if 'variant' in data:
                    info['game_variant'] = data['variant']
                if 'type' in data:
                    info['game_type'] = data['type']
                
                settings = data.get('settings', {})
                if settings:
                    if 'baseScore' in settings:
                        info['base_score'] = settings['baseScore']
                    if 'inMode' in settings:
                        info['in_mode'] = settings['inMode']
                    if 'outMode' in settings:
                        info['out_mode'] = settings['outMode']
                    if 'bullMode' in settings:
                        info['bull_mode'] = settings['bullMode']
                    if 'maxRounds' in settings:
                        info['max_rounds'] = settings['maxRounds']
                
                # Round, Leg, Set information
                if 'round' in data:
                    info['round'] = data['round']
                if 'leg' in data:
                    info['leg'] = data['leg']
                if 'legs' in data:
                    info['legs_total'] = data['legs']
                if 'set' in data:
                    info['set'] = data['set']
                
                # Scores (legs/sets won)
                scores = data.get('scores', [])
                if scores:
                    score_strings = []
                    for idx, score in enumerate(scores):
                        legs = score.get('legs', 0)
                        sets = score.get('sets', 0)
                        score_strings.append(f"P{idx}: {legs}L/{sets}S")
                    info['match_scores'] = ', '.join(score_strings)
                
                # Current player
                if 'player' in data:
                    info['current_player'] = data['player']
                
                # Player information
                players = data.get('players', [])
                if players:
                    player_names = [p.get('name', 'Unknown') for p in players]
                    info['players'] = ', '.join(player_names)
                    
                    # Board names
                    board_names = [p.get('boardName', '') for p in players if p.get('boardName')]
                    if board_names:
                        info['board_names'] = ', '.join(board_names)
                
                # Scores remaining
                game_scores = data.get('gameScores', [])
                if game_scores:
                    info['scores_remaining'] = ', '.join(map(str, game_scores))
                
                # Turn information
                if 'turnScore' in data:
                    info['turn_score'] = data['turnScore']
                if 'turnBusted' in data:
                    info['turn_busted'] = data['turnBusted']
                
                # Extract throws from current turn
                turns = data.get('turns', [])
                if turns:
                    current_turn = turns[-1]  # Last turn is current
                    throws = current_turn.get('throws', [])
                    
                    if throws:
                        throw_list = []
                        for throw in throws:
                            segment = throw.get('segment', {})
                            throw_name = segment.get('name', '?')
                            entry = throw.get('entry', 'detected')
                            
                            # Add AI validation marker
                            if 'corrected' in throw:
                                original = throw['corrected'].get('segment', {}).get('name', '?')
                                throw_name += f' (was {original})'
                            elif 'referee_ai_corrected' in entry:
                                throw_name += ' (AI✓)'
                            elif 'referee_ai_confirmed' in entry:
                                throw_name += ' (AI✓)'
                            elif 'manual' in entry:
                                throw_name += ' (manual)'
                            elif 'rejected' in entry:
                                throw_name += ' (rejected)'
                            
                            throw_list.append(throw_name)
                        
                        info['throws'] = ', '.join(throw_list)
                        info['darts_thrown'] = len(throws)
                    
                    # Turn points
                    if 'points' in current_turn:
                        info['turn_points'] = current_turn['points']
                    if 'busted' in current_turn:
                        info['turn_busted'] = current_turn['busted']
                
                # Checkout guide
                checkout = data.get('state', {}).get('checkoutGuide', [])
                if checkout:
                    checkout_names = [c.get('name', '?') for c in checkout]
                    info['checkout_guide'] = ' → '.join(checkout_names)
                
                # Statistics
                stats = data.get('stats', [])
                if stats and len(stats) > 0:
                    player_stats = stats[0]
                    match_stats = player_stats.get('matchStats', {})
                    if match_stats:
                        if 'average' in match_stats:
                            info['avg_3dart'] = f"{match_stats['average']:.2f}"
                        if 'first9Average' in match_stats:
                            info['first9_avg'] = f"{match_stats['first9Average']:.2f}"
                        if 'checkoutPercent' in match_stats:
                            info['checkout_pct'] = f"{match_stats['checkoutPercent']*100:.1f}%"
                        if 'checkouts' in match_stats and 'checkoutsHit' in match_stats:
                            info['checkouts'] = f"{match_stats['checkoutsHit']}/{match_stats['checkouts']}"
                        if 'total180' in match_stats and match_stats['total180'] > 0:
                            info['total_180s'] = match_stats['total180']
                        if 'plus100' in match_stats and match_stats['plus100'] > 0:
                            info['scores_100+'] = match_stats['plus100']
                        if 'dartsThrown' in match_stats:
                            info['darts_thrown_total'] = match_stats['dartsThrown']
            
            # Board events
            elif channel == 'autodarts.boards':
                topic = message_dict.get('topic', '')
                
                if '.events' in topic:
                    board_event = data.get('event', event)
                    if board_event:
                        info['board_event'] = board_event
                    
                    # Throw information for "Throw detected" events
                    if board_event == 'Throw detected':
                        throw = data.get('throw', {})
                        segment = throw.get('segment', {})
                        
                        if 'name' in segment:
                            info['thrown_segment'] = segment['name']
                        if 'multiplier' in segment:
                            info['multiplier'] = segment['multiplier']
                        if 'number' in segment:
                            info['number'] = segment['number']
                        if 'bed' in segment:
                            info['bed_type'] = segment['bed']
                        
                        # Throw number (1st, 2nd, or 3rd dart)
                        if 'throwNumber' in data:
                            info['throw_number'] = data['throwNumber']
                        
                        # Coordinates
                        coords = throw.get('coords', {})
                        if coords and 'x' in coords and 'y' in coords:
                            info['coords'] = f"({coords['x']:.3f}, {coords['y']:.3f})"
                
                # Match events (start, finish, etc.)
                elif '.matches' in topic:
                    match_event = data.get('event', event)
                    if match_event:
                        info['match_event'] = match_event
                    if 'id' in data:
                        info['match_id'] = data['id']
            
        except Exception as e:
            info['extraction_error'] = str(e)
        
        return info


# Global logger instance
_logger = None


def init_logger(enabled=False, log_dir="logs"):
    """Initialize the global message logger"""
    global _logger
    _logger = MessageLogger(enabled=enabled, log_dir=log_dir)
    return _logger


def get_logger():
    """Get the global message logger instance"""
    global _logger
    if _logger is None:
        _logger = MessageLogger(enabled=False)
    return _logger
