#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base parser module for code parsing.
This module provides a base class for all language-specific parsers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseParser(ABC):
    """
    Base abstract class for code parsers.
    All language-specific parsers should inherit from this class.
    """

    def __init__(self, file_path: str):
        """
        Initialize the parser with a file path.

        Args:
            file_path: Path to the code file to parse.
        """
        self.file_path = file_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        """
        Read the content of the file.

        Returns:
            str: The content of the file.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {self.file_path}: {str(e)}")
            return ""

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Parse the code file and extract structured information.
        
        Returns:
            Dict[str, Any]: A dictionary containing structured information about the code.
        """
        pass

    @abstractmethod
    def get_classes(self) -> List[Dict[str, Any]]:
        """
        Extract classes information from the code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a class.
        """
        pass

    @abstractmethod
    def get_methods(self) -> List[Dict[str, Any]]:
        """
        Extract methods information from the code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a method.
        """
        pass

    @abstractmethod
    def get_properties(self) -> List[Dict[str, Any]]:
        """
        Extract properties information from the code.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing information about a property.
        """
        pass
