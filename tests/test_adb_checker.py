import pytest
from unittest.mock import patch, MagicMock
import subprocess

from src.adb_checker import (
    is_adb_installed,
    get_connected_devices,
    check_adb_connectivity,
    check_adb_status,
    wait_for_device
)


class TestAdbChecker:
    
    @patch('subprocess.run')
    def test_is_adb_installed_success(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=0)
        
        # Test
        result = is_adb_installed()
        
        # Assert
        assert result is True
        mock_run.assert_called_once_with(
            ["adb", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
    
    @patch('subprocess.run')
    def test_is_adb_installed_not_found(self, mock_run):
        # Setup
        mock_run.side_effect = FileNotFoundError()
        
        # Test
        result = is_adb_installed()
        
        # Assert
        assert result is False
    
    @patch('subprocess.run')
    def test_is_adb_installed_timeout(self, mock_run):
        # Setup
        mock_run.side_effect = subprocess.TimeoutExpired(["adb", "version"], 10)
        
        # Test
        result = is_adb_installed()
        
        # Assert
        assert result is False
    
    @patch('subprocess.run')
    def test_get_connected_devices_with_devices(self, mock_run):
        # Setup
        mock_output = "List of devices attached\ndevice1\tdevice\ndevice2\tdevice\n"
        mock_run.return_value = MagicMock(returncode=0, stdout=mock_output)
        
        # Test
        success, devices = get_connected_devices()
        
        # Assert
        assert success is True
        assert devices == ["device1", "device2"]
    
    @patch('subprocess.run')
    def test_get_connected_devices_no_devices(self, mock_run):
        # Setup
        mock_output = "List of devices attached\n"
        mock_run.return_value = MagicMock(returncode=0, stdout=mock_output)
        
        # Test
        success, devices = get_connected_devices()
        
        # Assert
        assert success is True
        assert devices == []
    
    @patch('subprocess.run')
    def test_get_connected_devices_with_unauthorized_device(self, mock_run):
        # Setup - device is connected but not authorized
        mock_output = "List of devices attached\ndevice1\tunauthorized\n"
        mock_run.return_value = MagicMock(returncode=0, stdout=mock_output)
        
        # Test
        success, devices = get_connected_devices()
        
        # Assert
        assert success is True
        assert devices == []  # unauthorized devices are not included
    
    @patch('subprocess.run')
    def test_get_connected_devices_command_fails(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=1)
        
        # Test
        success, devices = get_connected_devices()
        
        # Assert
        assert success is False
        assert devices == []
    
    @patch('subprocess.run')
    def test_check_adb_connectivity_success(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=0, stdout="test\n")
        
        # Test
        result = check_adb_connectivity()
        
        # Assert
        assert result is True
        mock_run.assert_called_once_with(
            ["adb", "shell", "echo", "test"],
            capture_output=True,
            text=True,
            timeout=10
        )
    
    @patch('subprocess.run')
    def test_check_adb_connectivity_fails(self, mock_run):
        # Setup
        mock_run.return_value = MagicMock(returncode=1)
        
        # Test
        result = check_adb_connectivity()
        
        # Assert
        assert result is False
    
    @patch('src.adb_checker.check_adb_connectivity')
    @patch('src.adb_checker.get_connected_devices')
    @patch('src.adb_checker.is_adb_installed')
    def test_check_adb_status_all_good(self, mock_installed, mock_devices, mock_connectivity):
        # Setup
        mock_installed.return_value = True
        mock_devices.return_value = (True, ["device1"])
        mock_connectivity.return_value = True
        
        # Test
        is_ready, message = check_adb_status()
        
        # Assert
        assert is_ready is True
        assert "ADB is ready" in message
        assert "device1" in message
    
    @patch('src.adb_checker.is_adb_installed')
    def test_check_adb_status_adb_not_installed(self, mock_installed):
        # Setup
        mock_installed.return_value = False
        
        # Test
        is_ready, message = check_adb_status()
        
        # Assert
        assert is_ready is False
        assert "not installed" in message
    
    @patch('src.adb_checker.get_connected_devices')
    @patch('src.adb_checker.is_adb_installed')
    def test_check_adb_status_no_devices(self, mock_installed, mock_devices):
        # Setup
        mock_installed.return_value = True
        mock_devices.return_value = (True, [])
        
        # Test
        is_ready, message = check_adb_status()
        
        # Assert
        assert is_ready is False
        assert "No Android devices connected" in message
    
    @patch('src.adb_checker.check_adb_connectivity')
    @patch('src.adb_checker.get_connected_devices')
    @patch('src.adb_checker.is_adb_installed')
    def test_check_adb_status_connectivity_fails(self, mock_installed, mock_devices, mock_connectivity):
        # Setup
        mock_installed.return_value = True
        mock_devices.return_value = (True, ["device1"])
        mock_connectivity.return_value = False
        
        # Test
        is_ready, message = check_adb_status()
        
        # Assert
        assert is_ready is False
        assert "unable to communicate" in message
    
    @patch('time.sleep')
    @patch('src.adb_checker.check_adb_status')
    def test_wait_for_device_success_immediately(self, mock_check, mock_sleep):
        # Setup
        mock_check.return_value = (True, "ADB is ready")
        
        # Test
        result = wait_for_device(timeout_seconds=5)
        
        # Assert
        assert result is True
        mock_sleep.assert_not_called()
    
    @patch('time.time')
    @patch('time.sleep')
    @patch('src.adb_checker.check_adb_status')
    def test_wait_for_device_timeout(self, mock_check, mock_sleep, mock_time):
        # Setup - simulate time progression
        mock_time.side_effect = [0, 31]  # Start at 0, then jump to 31 seconds
        mock_check.return_value = (False, "No devices")
        
        # Test
        result = wait_for_device(timeout_seconds=30)
        
        # Assert
        assert result is False