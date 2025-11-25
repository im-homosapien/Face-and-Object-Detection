"""
Input Handler Module - Keyboard Input Management

This module manages all keyboard input for the face recognition system,
including face selection, text input for naming, and application control.

Features:
    - Face selection via number keys (1-9)
    - Text input for naming faces
    - Input mode state management
    - Backspace and special key handling
    - Database integration for saving names

Input Modes:
    1. Normal Mode:
       - Press 1-9: Select ready face for naming
       - Press Q: Quit application
    
    2. Input Mode (naming a face):
       - Type characters: Build name
       - Backspace: Delete last character
       - Enter: Save name and add to database
       - Escape: Cancel naming

Keyboard Controls:
    - 1-9: Select face by number
    - A-Z, a-z, 0-9, space: Text input
    - Backspace: Delete character
    - Enter: Confirm input
    - Escape: Cancel input
    - Q: Quit (normal mode only)

State Management:
    - input_mode: Boolean flag for input mode
    - input_text: Current text being typed
    - current_face_id: ID of face being named
    - selected_number: Display number of selected face

Usage:
    handler = InputHandler()
    key = cv2.waitKey(1) & 0xFF
    continue_running = handler.handle_key(key, results, database, tracker)

Author: Face & Object Detection System
Version: 2.0
"""


class InputHandler:
    """
    Manages keyboard input and input mode state.
    
    This class handles all keyboard interactions for the face recognition
    system, including face selection, text input for naming, and mode
    transitions. It maintains state for the current input operation.
    
    Attributes:
        input_mode (bool): True when user is typing a name
        input_text (str): Current text being entered
        current_face_id (int): ID of face being named
        selected_number (int): Display number (1-9) of selected face
    
    State Transitions:
        Normal → Input: User presses 1-9 to select ready face
        Input → Normal: User presses Enter (save) or Escape (cancel)
    
    Methods:
        - handle_key: Process keyboard input
        - is_in_input_mode: Check if in input mode
        - get_input_text: Get current input text
        - get_selected_number: Get selected face number
    """
    
    def __init__(self):
        """
        Initialize input handler with default state.
        
        Sets up the input handler in normal mode (not naming a face)
        with empty text and no face selected.
        
        Initial State:
            - input_mode: False (normal mode)
            - input_text: "" (empty)
            - current_face_id: None (no face selected)
            - selected_number: 0 (no selection)
        """
        self.input_mode = False        # Not in naming mode
        self.input_text = ""           # No text entered
        self.current_face_id = None    # No face selected
        self.selected_number = 0       # No selection number
    
    def handle_key(self, key, results, database, tracker):
        """
        Handle keyboard input with face selection and naming support.
        
        This is the main input processing method that handles all keyboard
        interactions. It operates in two modes: normal mode (face selection)
        and input mode (text entry for naming).
        
        Normal Mode (input_mode = False):
            - Keys 1-9: Select ready face for naming
            - Key Q: Quit application
        
        Input Mode (input_mode = True):
            - Enter: Save name and add to database
            - Escape: Cancel naming
            - Backspace: Delete last character
            - Printable chars: Add to name
        
        Args:
            key (int): Key code from cv2.waitKey() (0-255)
                Use: key = cv2.waitKey(1) & 0xFF
            results (list): Current frame detection results
                Each result should have 'status', 'face_id', 'selection_number'
            database (FaceDatabase): Database instance for saving faces
            tracker (FaceTracker): Tracker instance for getting embeddings
        
        Returns:
            bool: True to continue application, False to quit
        
        Key Codes:
            - 8: Backspace
            - 13: Enter
            - 27: Escape
            - 32-126: Printable ASCII characters
            - 49-57: Number keys 1-9
            - 113: 'q' key
        
        Example:
            >>> key = cv2.waitKey(1) & 0xFF
            >>> if not handler.handle_key(key, results, db, tracker):
            >>>     break  # Quit application
        
        Side Effects:
            - Modifies input_mode, input_text, current_face_id, selected_number
            - Adds faces to database when Enter pressed
            - Removes faces from tracker after naming
            - Prints status messages to console
        """
        # INPUT MODE: User is typing a name
        if self.input_mode:
            if key == 13:  # Enter key - save name
                if self.input_text.strip():
                    # Get all collected embeddings for this face
                    embeddings = tracker.get_embeddings(self.current_face_id)
                    
                    # Add person to database with averaged embedding
                    database.add_person(self.input_text.strip(), embeddings)
                    
                    # Remove from tracker (no longer unknown)
                    tracker.remove_face(self.current_face_id)
                    
                    print(f"✓ Added: {self.input_text.strip()}")
                    
                    # Reset to normal mode
                    self.input_mode = False
                    self.input_text = ""
                    self.current_face_id = None
                    self.selected_number = 0
            
            elif key == 27:  # Escape key - cancel naming
                print("Cancelled naming")
                # Reset to normal mode without saving
                self.input_mode = False
                self.input_text = ""
                self.current_face_id = None
                self.selected_number = 0
            
            elif key == 8:  # Backspace - delete last character
                self.input_text = self.input_text[:-1]
            
            elif 32 <= key <= 126:  # Printable ASCII characters
                # Add character to input text
                self.input_text += chr(key)
        
        # NORMAL MODE: User can select faces or quit
        else:
            # Check for face selection (keys 1-9)
            if 49 <= key <= 57:  # ASCII codes for '1' to '9'
                selection_num = key - 48  # Convert ASCII to number (1-9)
                
                # Find face with this selection number
                for result in results:
                    if result.get('status') == 'ready' and \
                       result.get('selection_number') == selection_num:
                        # Enter input mode for this face
                        self.input_mode = True
                        self.current_face_id = result['face_id']
                        self.selected_number = selection_num
                        self.input_text = ""
                        print(f"\n>>> Selected face #{selection_num} - Type name and press ENTER")
                        break
            
            elif key == ord('q'):  # Quit application
                return False
        
        return True  # Continue running
    
    def is_in_input_mode(self):
        """
        Check if currently in input mode (naming a face).
        
        Used by UI renderer to determine whether to display the input overlay.
        
        Returns:
            bool: True if in input mode, False if in normal mode
        
        Example:
            >>> if handler.is_in_input_mode():
            >>>     renderer.draw_input_box(frame, handler.get_input_text())
        """
        return self.input_mode
    
    def get_input_text(self):
        """
        Get the current text being entered by the user.
        
        Returns the text that the user has typed so far when naming a face.
        
        Returns:
            str: Current input text (may be empty)
        
        Example:
            >>> text = handler.get_input_text()
            >>> print(f"User typed: {text}")
            User typed: Joh
        """
        return self.input_text
    
    def get_selected_number(self):
        """
        Get the selection number of the face being named.
        
        Returns the display number (1-9) of the face that was selected
        for naming. Used by UI to show which face is being named.
        
        Returns:
            int: Selection number (1-9), or 0 if no face selected
        
        Example:
            >>> num = handler.get_selected_number()
            >>> print(f"Naming face #{num}")
            Naming face #1
        """
        return self.selected_number
