import pytest
from unittest.mock import patch, MagicMock
import subprocess

from src.adb_commands import send_adb_tap, turn_screen_off, send_adb_keyevent


class TestAdbCommands:
    
    @patch('subprocess.run')
    def test_send_adb_tap_success(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        # Test
        result = send_adb_tap(100, 200)
        
        # Assert
        assert result is True
        mock_run.assert_called_once_with(
            ["adb", "shell", "input", "tap", "100", "200"],
            capture_output=True,
            text=True,
            timeout=10
        )
    
    @patch('subprocess.run')
    def test_send_adb_tap_failure(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=1, stderr="error message")
        
        # Test
        result = send_adb_tap(100, 200)
        
        # Assert
        assert result is False
    
    @patch('subprocess.run')
    def test_send_adb_tap_timeout(self, mock_run):
        # Setup
        mock_run.side_effect = subprocess.TimeoutExpired(["adb"], 10)
        
        # Test
        result = send_adb_tap(100, 200)
        
        # Assert
        assert result is False
    
    @patch('subprocess.run')
    def test_send_adb_tap_file_not_found(self, mock_run):
        # Setup
        mock_run.side_effect = FileNotFoundError()
        
        # Test
        result = send_adb_tap(100, 200)
        
        # Assert
        assert result is False
    
    @patch('subprocess.run')
    def test_turn_screen_off_success(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        # Test
        result = turn_screen_off()
        
        # Assert
        assert result is True
        mock_run.assert_called_once_with(
            ["adb", "shell", "input", "keyevent", "26"],
            capture_output=True,
            text=True,
            timeout=10
        )
    
    @patch('subprocess.run')
    def test_turn_screen_off_failure(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=1, stderr="error message")
        
        # Test
        result = turn_screen_off()
        
        # Assert
        assert result is False
    
    @patch('subprocess.run')
    def test_send_adb_keyevent_success(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        # Test
        result = send_adb_keyevent(4)  # Back button
        
        # Assert
        assert result is True
        mock_run.assert_called_once_with(
            ["adb", "shell", "input", "keyevent", "4"],
            capture_output=True,
            text=True,
            timeout=10
        )
    
    @patch('subprocess.run')
    def test_send_adb_keyevent_failure(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=1, stderr="error message")
        
        # Test
        result = send_adb_keyevent(4)
        
        # Assert
        assert result is False