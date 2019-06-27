#!/usr/bin/python3
"""Module creates custom storage variable"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
