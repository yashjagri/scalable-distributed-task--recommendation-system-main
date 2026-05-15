import json
import signal
import sys
import time
from collections import defaultdict
from typing import Dict, Tuple, Optional

from kafka import KafkaConsumer

from app import config
from app.db import SessionLocal
from app.repositories import RecommendationRepository