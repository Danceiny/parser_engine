from . import patch
from .request import TaskRequest
from .decorator import Template
from .singleton import Singleton, ThreadSafeSingleton
from .template import PEField, PETemplate

TemplateAnnotation = Template()

__all__ = ['TemplateAnnotation', 'TaskRequest', 'Singleton', 'ThreadSafeSingleton', 'PEField', 'PETemplate']
