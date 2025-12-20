---
sidebar_position: 2
---

# Chapter 1: Voice-to-Action with OpenAI Whisper

This chapter covers speech recognition using OpenAI Whisper, natural language processing, and command execution for humanoid robots, enabling voice-controlled interaction and behavior using state-of-the-art voice recognition technology.

## Learning Objectives

- Understand the fundamentals of voice-to-action systems for robotics
- Implement speech recognition and processing for robot commands
- Design natural language understanding for command interpretation
- Map voice commands to robot actions and behaviors
- Integrate voice control with ROS 2 navigation and manipulation systems
- Create robust voice command processing pipelines

## Table of Contents

1. [Introduction to Voice-to-Action Systems](#introduction-to-voice-to-action-systems)
2. [Speech Recognition and Processing](#speech-recognition-and-processing)
3. [Natural Language Understanding for Commands](#natural-language-understanding-for-commands)
4. [Voice Command Mapping to Robot Actions](#voice-command-mapping-to-robot-actions)
5. [Integration with ROS 2 Systems](#integration-with-ros-2-systems)
6. [Practical Examples](#practical-examples)
7. [Summary and Next Steps](#summary-and-next-steps)

## Conceptual Overview

Before diving into the technical implementation, it's important to understand the fundamental concepts behind voice-to-action systems using OpenAI Whisper for humanoid robots:

- **Voice-to-Action Systems**: The integration of speech recognition using OpenAI Whisper, natural language processing, and robot control to enable voice-controlled robot behaviors
- **OpenAI Whisper**: A state-of-the-art speech recognition model that converts spoken language into text with high accuracy across multiple languages and accents
- **Speech Recognition Pipeline**: The process of capturing audio, processing it through Whisper, and converting it to text for further processing
- **Natural Language Understanding (NLU)**: The ability to interpret the meaning and intent behind natural language commands extracted from Whisper
- **Command Mapping**: The process of translating high-level voice commands into specific robot actions
- **Intent Recognition**: Identifying the user's intended action or goal from Whisper-processed voice commands
- **Action Execution**: The process of executing robot behaviors based on interpreted voice commands

These concepts form the foundation of voice-controlled robotics using OpenAI Whisper, enabling intuitive human-robot interaction through natural language.

## Introduction to Voice-to-Action Systems

Voice-to-action systems represent a crucial advancement in human-robot interaction, allowing users to communicate with robots using natural language. For humanoid robots, voice interfaces provide an intuitive and accessible way to control complex behaviors without requiring specialized knowledge of robot programming or interfaces.

### The Voice Command Pipeline

A typical voice-to-action system follows this pipeline:

1. **Audio Capture**: Microphones capture the user's voice command
2. **Speech Recognition**: Audio is converted to text using speech-to-text algorithms
3. **Natural Language Understanding**: The text is analyzed to extract intent and parameters
4. **Command Mapping**: Intents are mapped to specific robot actions or behaviors
5. **Action Execution**: The robot executes the mapped actions using its control systems
6. **Feedback**: The robot provides feedback to confirm command receipt and execution

This pipeline enables robots to understand and respond to natural language commands, creating a seamless interaction experience for users.

### Applications in Humanoid Robotics

Voice-to-action systems are particularly valuable for humanoid robots due to their human-like form factor. Users naturally expect to interact with humanoid robots using voice commands, making voice interfaces a key component of natural human-robot interaction.

Common applications include:
- Navigation commands ("Go to the kitchen")
- Manipulation tasks ("Pick up the red cup")
- Information requests ("What time is it?")
- Complex multi-step instructions ("Go to John's office and tell him to join the meeting")

## Speech Recognition and Processing

### OpenAI Whisper for Robotics

OpenAI Whisper is a state-of-the-art speech recognition model that provides exceptional accuracy across multiple languages and accents. For robotics applications, Whisper offers both local processing capabilities and robust performance in diverse acoustic environments.

#### Whisper Model Options

Whisper provides several model sizes optimized for different use cases in robotics:

- **tiny**: Fastest processing, suitable for real-time applications with limited computational resources
- **base**: Good balance between speed and accuracy
- **small**: Better accuracy with moderate computational requirements
- **medium**: High accuracy suitable for most robotics applications
- **large**: Highest accuracy but requires significant computational resources

#### Local Whisper Implementation

For robotics applications, local Whisper processing provides better privacy and reduced latency:

```python
import whisper
import torch
import pyaudio
import wave
import numpy as np
import rospy
from std_msgs.msg import String

class WhisperRecognizer:
    def __init__(self, model_size="base"):
        # Load Whisper model
        self.model = whisper.load_model(model_size)

        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1

        # Initialize audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = None

        # Publisher for recognized text
        self.text_pub = rospy.Publisher('recognized_text', String, queue_size=10)

    def start_listening(self):
        """Start audio stream for voice capture"""
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        rospy.loginfo("Whisper voice recognition started")

    def stop_listening(self):
        """Stop audio stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        rospy.loginfo("Whisper voice recognition stopped")

    def record_audio_chunk(self, duration=3):
        """Record a chunk of audio for processing"""
        frames = []

        for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
            data = self.stream.read(self.chunk_size)
            frames.append(data)

        # Save to temporary WAV file for Whisper processing
        audio_data = b''.join(frames)
        return self._bytes_to_wav(audio_data)

    def _bytes_to_wav(self, audio_bytes):
        """Convert audio bytes to WAV format for Whisper"""
        # Create temporary WAV file
        import tempfile
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)

        wf = wave.open(temp_wav.name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(audio_bytes)
        wf.close()

        return temp_wav.name

    def transcribe_audio(self, audio_file_path):
        """Transcribe audio using Whisper model"""
        try:
            # Load audio file
            audio = whisper.load_audio(audio_file_path)
            audio = whisper.pad_or_trim(audio)

            # Make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            # Decode the audio
            options = whisper.DecodingOptions()
            result = whisper.decode(self.model, mel, options)

            return result.text
        except Exception as e:
            rospy.logerr(f"Whisper transcription error: {e}")
            return None

    def continuous_recognition(self):
        """Continuously listen and recognize speech"""
        self.start_listening()

        try:
            while not rospy.is_shutdown():
                # Record audio chunk
                audio_file = self.record_audio_chunk(duration=3)

                # Transcribe using Whisper
                text = self.transcribe_audio(audio_file)

                if text and text.strip():
                    # Publish recognized text
                    text_msg = String()
                    text_msg.data = text.strip()
                    self.text_pub.publish(text_msg)

                    rospy.loginfo(f"Whisper recognized: {text}")

                # Clean up temporary file
                import os
                os.unlink(audio_file)

        except KeyboardInterrupt:
            rospy.loginfo("Whisper recognition interrupted")
        finally:
            self.stop_listening()
```

#### Whisper with ROS 2 Integration

For ROS 2 applications, Whisper can be integrated as a dedicated node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import whisper
import pyaudio
import wave
import tempfile
import os

class WhisperNode(Node):
    def __init__(self):
        super().__init__('whisper_node')

        # Load Whisper model
        self.model = whisper.load_model("base")

        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1

        # Initialize audio
        self.audio = pyaudio.PyAudio()
        self.stream = None

        # Publishers and subscribers
        self.recognized_text_pub = self.create_publisher(String, 'recognized_speech', 10)
        self.activation_sub = self.create_subscription(String, 'voice_activation',
                                                      self.activation_callback, 10)

        # Activation state
        self.is_listening = False

        self.get_logger().info('Whisper node initialized')

    def activation_callback(self, msg):
        """Handle activation messages"""
        if msg.data.lower() == 'start':
            self.start_listening()
        elif msg.data.lower() == 'stop':
            self.stop_listening()

    def start_listening(self):
        """Start audio stream"""
        if not self.is_listening:
            try:
                self.stream = self.audio.open(
                    format=self.audio_format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=self.chunk_size
                )
                self.is_listening = True
                self.get_logger().info("Whisper listening started")

                # Start recognition thread
                import threading
                self.recognition_thread = threading.Thread(target=self._continuous_recognition)
                self.recognition_thread.daemon = True
                self.recognition_thread.start()

            except Exception as e:
                self.get_logger().error(f"Failed to start audio stream: {e}")

    def stop_listening(self):
        """Stop audio stream"""
        self.is_listening = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.get_logger().info("Whisper listening stopped")

    def _continuous_recognition(self):
        """Internal method for continuous recognition"""
        while self.is_listening:
            try:
                # Record audio chunk
                frames = []
                for _ in range(0, int(self.sample_rate / self.chunk_size * 3)):  # 3 seconds
                    data = self.stream.read(self.chunk_size)
                    frames.append(data)

                # Process audio
                audio_data = b''.join(frames)

                # Save to temporary file
                temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                wf = wave.open(temp_wav.name, 'wb')
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data)
                wf.close()

                # Transcribe with Whisper
                result = self.model.transcribe(temp_wav.name)
                text = result["text"].strip()

                if text:
                    # Publish recognized text
                    text_msg = String()
                    text_msg.data = text
                    self.recognized_text_pub.publish(text_msg)
                    self.get_logger().info(f"Recognized: {text}")

                # Clean up
                os.unlink(temp_wav.name)

            except Exception as e:
                self.get_logger().error(f"Recognition error: {e}")

                # Clean up temp file if it exists
                try:
                    os.unlink(temp_wav.name)
                except:
                    pass

    def destroy_node(self):
        """Clean up resources"""
        self.stop_listening()
        self.audio.terminate()
        super().destroy_node()
```

### Audio Preprocessing for Whisper in Robotics

Robot environments often present unique challenges for speech recognition, including background noise from motors, fans, and other equipment. Effective audio preprocessing is crucial for reliable Whisper-based voice command recognition. Whisper is quite robust to noise, but preprocessing can still improve recognition quality.

#### Preprocessing Pipeline for Whisper

Whisper works best with audio at 16kHz sample rate. The preprocessing pipeline should ensure proper audio format:

```python
import numpy as np
from scipy import signal
import librosa

class WhisperAudioPreprocessor:
    def __init__(self):
        self.target_sample_rate = 16000
        self.noise_threshold = 0.01

    def preprocess_for_whisper(self, audio_data, original_sample_rate):
        """Preprocess audio data specifically for Whisper"""
        # Resample to Whisper's expected rate (16kHz)
        if original_sample_rate != self.target_sample_rate:
            audio_data = librosa.resample(audio_data.astype(np.float32),
                                         orig_sr=original_sample_rate,
                                         target_sr=self.target_sample_rate)

        # Normalize volume
        normalized = self.normalize_volume(audio_data)

        # Apply high-pass filter to remove low-frequency noise (optional)
        filtered = self.high_pass_filter(normalized, self.target_sample_rate)

        return filtered

    def normalize_volume(self, audio_data):
        """Normalize audio volume to consistent level"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data

    def high_pass_filter(self, audio_data, sample_rate, cutoff_freq=100):
        """Apply high-pass filter to remove low-frequency noise"""
        nyquist = sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype='high', analog=False)
        filtered = signal.filtfilt(b, a, audio_data)
        return filtered
```


### Wake Word Detection with Whisper Integration

For always-listening systems, wake word detection allows the robot to activate only when specifically addressed, reducing processing load and privacy concerns. For Whisper-based systems, wake word detection can be implemented using lightweight audio analysis that triggers the full Whisper pipeline only when needed.

#### Lightweight Wake Word Detection

Since Whisper is computationally intensive, it's important to implement efficient wake word detection that only activates Whisper when necessary:

```python
import numpy as np
from scipy.io import wavfile
import pyaudio
import threading
import queue

class WhisperWakeWordDetector:
    def __init__(self, wake_word="robot", activation_threshold=0.7):
        self.wake_word = wake_word.lower()
        self.activation_threshold = activation_threshold
        self.activation_queue = queue.Queue()
        self.is_active = False
        self.activation_callback = None

    def detect_wake_word(self, audio_sample):
        """Detect if wake word is present in audio sample using simple pattern matching"""
        # This is a simplified approach - in practice, you'd use a dedicated wake word model
        # or lightweight neural network for better accuracy

        # For Whisper integration, this would analyze the audio for wake word patterns
        # before activating the full Whisper pipeline
        return self._simple_wake_word_detection(audio_sample)

    def _simple_wake_word_detection(self, audio_sample):
        """Simple audio pattern matching for wake word detection"""
        # Calculate audio energy to detect speech
        energy = np.sum(audio_sample ** 2) / len(audio_sample)

        # If energy is above threshold, we have speech - trigger Whisper
        # In a real implementation, this would use a proper wake word model
        if energy > 0.001:  # Adjust threshold based on your environment
            return True, energy
        return False, energy

    def set_activation_callback(self, callback):
        """Set callback function to be called when wake word is detected"""
        self.activation_callback = callback

    def continuous_detection(self):
        """Continuously listen for wake word"""
        # Audio setup for wake word detection
        chunk_size = 1024
        sample_rate = 16000
        audio_format = pyaudio.paInt16
        channels = 1

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=audio_format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size
        )

        try:
            while True:
                # Read audio chunk
                data = stream.read(chunk_size)
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

                # Check for wake word
                detected, confidence = self.detect_wake_word(audio_data)

                if detected and confidence > self.activation_threshold:
                    if self.activation_callback:
                        self.activation_callback()
        except KeyboardInterrupt:
            print("Wake word detection stopped")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
```


## Natural Language Understanding for Commands

### Intent Recognition with LLMs and Whisper Output

Large Language Models (LLMs) excel at understanding the intent behind natural language commands extracted from Whisper transcription. By framing the intent recognition task as a structured prompt, we can leverage LLMs to accurately parse Whisper's transcribed text for robot command interpretation.

#### Processing Whisper Transcription with LLMs

Whisper provides high-quality text transcription that can be further processed by LLMs for intent recognition and command interpretation:

```python
import openai
import json
import re
import rospy
from std_msgs.msg import String

class WhisperLLMIntentRecognizer:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.intent_definitions = {
            "navigation": {
                "keywords": ["go to", "move to", "navigate", "walk to", "travel to"],
                "parameters": ["destination"]
            },
            "manipulation": {
                "keywords": ["pick up", "grasp", "take", "grab", "lift"],
                "parameters": ["object", "location"]
            },
            "information": {
                "keywords": ["tell me", "what time", "current", "information"],
                "parameters": ["topic"]
            }
        }

    def extract_intent_and_parameters(self, whisper_transcription):
        """Use LLM to extract intent and parameters from Whisper transcription"""
        # Validate that we have meaningful transcription from Whisper
        if not whisper_transcription or len(whisper_transcription.strip()) < 2:
            return None

        prompt = f"""
        You are a robot command parser processing text transcribed from speech using OpenAI Whisper.
        Parse the following command and extract the intent and parameters.

        Whisper Transcription: "{whisper_transcription}"

        Possible intents: navigation, manipulation, information, other

        Return JSON in the format:
        {{
            "intent": "intent_type",
            "parameters": {{
                "param_name": "param_value"
            }},
            "confidence": 0.0-1.0
        }}

        Be precise and only return the JSON object.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )

            # Extract JSON from response
            response_text = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                # Fallback to simple keyword matching if JSON parsing fails
                return self.fallback_intent_extraction(whisper_transcription)

        except Exception as e:
            rospy.logerr(f"LLM intent recognition failed: {e}")
            return self.fallback_intent_extraction(whisper_transcription)

    def fallback_intent_extraction(self, command_text):
        """Fallback intent extraction using keyword matching"""
        command_lower = command_text.lower()

        for intent, definition in self.intent_definitions.items():
            for keyword in definition["keywords"]:
                if keyword in command_lower:
                    return {
                        "intent": intent,
                        "parameters": self.extract_parameters(keyword, command_text),
                        "confidence": 0.7
                    }

        return {
            "intent": "other",
            "parameters": {"raw_command": command_text},
            "confidence": 0.5
        }

    def extract_parameters(self, matched_keyword, command_text):
        """Extract parameters based on matched keyword"""
        # Simple parameter extraction - in practice, this would be more sophisticated
        remaining_text = command_text.lower().replace(matched_keyword, "").strip()
        return {"action_detail": remaining_text}
```


### Named Entity Recognition for Whisper-Processed Commands

Named entity recognition (NER) is crucial for identifying specific objects, locations, and people mentioned in voice commands processed by OpenAI Whisper. Since Whisper provides clean text transcription, NER can effectively extract entities from the transcribed speech.

```python
class RobotNER:
    def __init__(self):
        self.known_objects = set([
            "cup", "bottle", "book", "phone", "keys", "ball",
            "red cup", "blue bottle", "large book", "small ball"
        ])

        self.known_locations = set([
            "kitchen", "living room", "bedroom", "office",
            "dining room", "bathroom", "hallway", "garage"
        ])

        self.known_people = set([
            "john", "mary", "tom", "sarah", "dad",
            "mom", "teacher", "boss", "friend"
        ])

    def extract_entities(self, command_text):
        """Extract named entities from command text"""
        entities = {
            "objects": [],
            "locations": [],
            "people": [],
            "other": []
        }

        text_lower = command_text.lower()

        # Extract objects
        for obj in self.known_objects:
            if obj in text_lower:
                entities["objects"].append(obj)

        # Extract locations
        for loc in self.known_locations:
            if loc in text_lower:
                entities["locations"].append(loc)

        # Extract people
        for person in self.known_people:
            if person in text_lower:
                entities["people"].append(person)

        return entities
```

### Context-Aware Command Understanding with Whisper Transcription

Contextual information enhances the understanding of voice commands processed by OpenAI Whisper by considering the current situation, location, and previous interactions. Whisper's accurate transcription provides clean text input for context-aware command interpretation.

```python
class ContextAwareParser:
    def __init__(self):
        self.current_context = {
            "location": "unknown",
            "time_of_day": "unknown",
            "recent_interactions": [],
            "robot_state": "idle",
            "visible_objects": []
        }

    def parse_with_context(self, command_text):
        """Parse command considering current context"""
        # Combine command with context for LLM processing
        context_description = self.format_context()
        full_prompt = f"""
        Context: {context_description}
        Command: {command_text}

        Interpret the command considering the context. If the command refers to
        objects or locations not explicitly mentioned but available in context,
        include them in the interpretation.

        Return JSON with intent, parameters, and confidence.
        """

        # Process with LLM (implementation similar to LLMIntentRecognizer)
        # This would call the LLM with the contextual prompt
        pass

    def format_context(self):
        """Format current context for LLM processing"""
        return f"""
        Location: {self.current_context['location']}
        Time: {self.current_context['time_of_day']}
        Robot State: {self.current_context['robot_state']}
        Visible Objects: {', '.join(self.current_context['visible_objects'])}
        Recent Interactions: {len(self.current_context['recent_interactions'])} interactions
        """

    def update_context(self, new_context_data):
        """Update the current context with new information"""
        self.current_context.update(new_context_data)
```

## Voice Command Mapping from Whisper Transcription to Robot Actions

### Action Mapping Architecture

The action mapping system translates high-level intents extracted from OpenAI Whisper transcriptions into specific robot behaviors and action sequences. This pipeline connects Whisper's speech-to-text capabilities with robotic action execution.

```python
from enum import Enum
from typing import Dict, Any, List
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import String

class ActionType(Enum):
    NAVIGATION = "navigation"
    MANIPULATION = "manipulation"
    COMMUNICATION = "communication"
    PERCEPTION = "perception"
    OTHER = "other"

class ActionMapper:
    def __init__(self):
        self.action_registry = {
            "navigation": self.handle_navigation,
            "manipulation": self.handle_manipulation,
            "communication": self.handle_communication,
            "information": self.handle_information_request
        }

        # Publishers for different robot systems
        self.nav_pub = rospy.Publisher('/move_base_simple/goal', Pose, queue_size=1)
        self.action_pub = rospy.Publisher('/robot_actions', String, queue_size=1)

    def map_and_execute(self, intent_result):
        """Map intent to action and execute"""
        intent = intent_result.get("intent", "other")
        parameters = intent_result.get("parameters", {})
        confidence = intent_result.get("confidence", 0.0)

        if confidence < 0.6:  # Low confidence threshold
            self.request_clarification(intent_result)
            return False

        handler = self.action_registry.get(intent)
        if handler:
            try:
                success = handler(parameters)
                self.log_action(intent, parameters, success)
                return success
            except Exception as e:
                rospy.logerr(f"Action execution failed: {e}")
                return False
        else:
            rospy.logwarn(f"No handler for intent: {intent}")
            return False

    def handle_navigation(self, parameters):
        """Handle navigation commands"""
        destination = parameters.get("destination", "")

        # Convert destination to known location
        target_pose = self.lookup_location(destination)
        if target_pose:
            self.nav_pub.publish(target_pose)
            rospy.loginfo(f"Navigating to {destination}")
            return True
        else:
            rospy.logwarn(f"Unknown destination: {destination}")
            return False

    def handle_manipulation(self, parameters):
        """Handle manipulation commands"""
        object_name = parameters.get("object", "")
        action = parameters.get("action", "grasp")

        # Look up object in perception system
        object_pose = self.find_object(object_name)
        if object_pose:
            command = {
                "action": action,
                "object": object_name,
                "pose": object_pose
            }
            self.action_pub.publish(str(command))
            rospy.loginfo(f"Attempting to {action} {object_name}")
            return True
        else:
            rospy.logwarn(f"Object not found: {object_name}")
            return False

    def handle_communication(self, parameters):
        """Handle communication commands"""
        message = parameters.get("message", "")
        recipient = parameters.get("recipient", "everyone")

        # Implement communication action
        self.communicate(message, recipient)
        return True

    def handle_information_request(self, parameters):
        """Handle information requests"""
        topic = parameters.get("topic", "")

        # Retrieve and communicate information
        info = self.retrieve_information(topic)
        self.communicate(info, "requester")
        return True

    def lookup_location(self, location_name):
        """Look up known location by name"""
        # This would interface with a location knowledge base
        known_locations = {
            "kitchen": self.create_pose(5.0, 3.0, 0.0),
            "living room": self.create_pose(0.0, 0.0, 0.0),
            "bedroom": self.create_pose(-3.0, 2.0, 0.0)
        }
        return known_locations.get(location_name.lower())

    def find_object(self, object_name):
        """Find object in perception system"""
        # This would interface with object recognition system
        # For demo purposes, return a fixed pose
        return self.create_pose(1.0, 1.0, 0.0)

    def create_pose(self, x, y, z):
        """Create a pose message"""
        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        # Set orientation to face forward (z-axis rotation)
        pose.orientation.z = 1.0  # 90-degree rotation around z-axis
        return pose

    def communicate(self, message, recipient):
        """Communicate message to recipient"""
        # Implementation for speech output, display, etc.
        rospy.loginfo(f"Communicating to {recipient}: {message}")

    def retrieve_information(self, topic):
        """Retrieve requested information"""
        # This would interface with knowledge base or sensors
        return f"I found information about {topic}."

    def log_action(self, intent, parameters, success):
        """Log action execution for learning and debugging"""
        rospy.loginfo(f"Action - Intent: {intent}, Params: {parameters}, Success: {success}")

    def request_clarification(self, intent_result):
        """Request clarification for low-confidence interpretations"""
        rospy.loginfo("Could you please repeat or clarify your command?")
```

### Multi-Step Command Handling

Complex voice commands often require multiple sequential actions, requiring sophisticated planning and execution management.

```python
class MultiStepCommandHandler:
    def __init__(self, action_mapper):
        self.action_mapper = action_mapper
        self.current_plan = []
        self.plan_execution_index = 0
        self.waiting_for_completion = False

    def handle_complex_command(self, intent_result):
        """Handle complex commands that require multiple steps"""
        intent = intent_result.get("intent", "other")

        if intent == "complex_task":
            # Generate multi-step plan
            self.current_plan = self.generate_plan(intent_result)
            self.plan_execution_index = 0
            return self.execute_next_step()
        else:
            # Handle simple command
            return self.action_mapper.map_and_execute(intent_result)

    def generate_plan(self, intent_result):
        """Generate a plan for complex commands"""
        parameters = intent_result.get("parameters", {})
        task_type = parameters.get("task_type", "")

        if task_type == "delivery":
            # Plan: navigate to pickup location -> pick up object -> navigate to destination -> deliver
            return [
                {
                    "intent": "navigation",
                    "parameters": {"destination": parameters.get("pickup_location", "")}
                },
                {
                    "intent": "manipulation",
                    "parameters": {
                        "action": "pick_up",
                        "object": parameters.get("object", "")
                    }
                },
                {
                    "intent": "navigation",
                    "parameters": {"destination": parameters.get("delivery_location", "")}
                },
                {
                    "intent": "manipulation",
                    "parameters": {
                        "action": "place_down",
                        "object": parameters.get("object", "")
                    }
                }
            ]
        else:
            # Default to single action
            return [intent_result]

    def execute_next_step(self):
        """Execute the next step in the plan"""
        if self.plan_execution_index >= len(self.current_plan):
            rospy.loginfo("Complex task completed")
            self.current_plan = []
            return True

        current_step = self.current_plan[self.plan_execution_index]
        success = self.action_mapper.map_and_execute(current_step)

        if success:
            self.plan_execution_index += 1
            # Continue to next step
            return self.execute_next_step()
        else:
            rospy.logerr("Failed to execute plan step, aborting task")
            self.current_plan = []
            return False
```

## Integration with ROS 2 Systems for Whisper-based Voice Control

### ROS 2 Node Implementation for Whisper

The Whisper-based voice-to-action system integrates with ROS 2 through a dedicated node that coordinates audio capture, Whisper processing, intent recognition, and robot action execution.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import AudioData
from geometry_msgs.msg import Pose
import threading
import queue
import whisper
import pyaudio
import wave
import numpy as np
import tempfile
import os

class WhisperVoiceToActionNode(Node):
    def __init__(self):
        super().__init__('whisper_voice_to_action_node')

        # Initialize Whisper components
        self.whisper_model = whisper.load_model("base")  # Can be tiny, base, small, medium, large
        self.whisper_preprocessor = WhisperAudioPreprocessor()
        self.intent_recognizer = WhisperLLMIntentRecognizer(api_key="your-openai-key-here")
        self.action_mapper = ActionMapper()
        self.multi_step_handler = MultiStepCommandHandler(self.action_mapper)

        # Publishers and subscribers
        self.command_pub = self.create_publisher(String, 'robot_commands', 10)
        self.audio_sub = self.create_subscription(AudioData, 'microphone/audio',
                                                 self.audio_callback, 10)
        self.voice_command_sub = self.create_subscription(String, 'voice_commands',
                                                         self.voice_command_callback, 10)

        # Service clients for other robot systems
        self.navigation_client = self.create_client(NavigateToPose, 'navigate_to_pose')

        # Threading for non-blocking processing
        self.command_queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.processing_thread.start()

        self.get_logger().info('Whisper-based Voice-to-Action node initialized')

    def audio_callback(self, msg):
        """Handle incoming audio data"""
        try:
            # Preprocess audio
            processed_audio = self.audio_preprocessor.preprocess_audio(msg.data)

            # Recognize speech
            text = self.speech_recognizer.recognize_from_processed_audio(processed_audio)

            if text:
                self.get_logger().info(f'Recognized: {text}')

                # Add to processing queue
                self.command_queue.put(text)

        except Exception as e:
            self.get_logger().error(f'Audio processing error: {e}')

    def voice_command_callback(self, msg):
        """Handle direct voice command messages (bypass Whisper if text already provided)"""
        self.command_queue.put(msg.data)

    def process_commands(self):
        """Process commands from queue in separate thread"""
        while rclpy.ok():
            try:
                command_text = self.command_queue.get(timeout=1.0)

                if command_text:
                    # Process Whisper transcription through intent recognition pipeline
                    intent_result = self.intent_recognizer.extract_intent_and_parameters(command_text)

                    if intent_result:
                        # Handle with multi-step handler
                        success = self.multi_step_handler.handle_complex_command(intent_result)

                        if success:
                            self.get_logger().info(f'Whisper command executed successfully: {command_text}')
                        else:
                            self.get_logger().warn(f'Whisper command execution failed: {command_text}')
                    else:
                        self.get_logger().warn(f'Could not parse Whisper transcription: {command_text}')

            except queue.Empty:
                continue
            except Exception as e:
                self.get_logger().error(f'Command processing error: {e}')

    def destroy_node(self):
        """Clean up resources"""
        if self.processing_thread.is_alive():
            self.processing_thread.join(timeout=1.0)
        super().destroy_node()
```

### Voice Command Interface

A clean interface allows other parts of the system to trigger voice processing programmatically.

```python
class VoiceInterface:
    def __init__(self, node):
        self.node = node
        self.active_listening = False
        self.wake_word_enabled = True

    def start_listening(self):
        """Start listening for voice commands"""
        self.active_listening = True
        self.node.get_logger().info("Voice command listening activated")

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.active_listening = False
        self.node.get_logger().info("Voice command listening deactivated")

    def process_direct_command(self, command_text):
        """Process a command without speech recognition"""
        intent_result = self.node.intent_recognizer.extract_intent_and_parameters(command_text)
        if intent_result:
            return self.node.multi_step_handler.handle_complex_command(intent_result)
        return False

    def enable_wake_word(self):
        """Enable wake word activation"""
        self.wake_word_enabled = True

    def disable_wake_word(self):
        """Disable wake word activation"""
        self.wake_word_enabled = False
```

## Practical Examples

### Example 1: Setting up Voice Command Processing

This example demonstrates how to set up a basic voice command processing system:

```bash
# Terminal 1: Start the robot system
ros2 launch my_humanoid_robot bringup.launch.py

# Terminal 2: Start the Whisper-based voice-to-action system
ros2 run whisper_voice_to_action whisper_voice_to_action_node

# Terminal 3: Send a voice command directly (for testing)
ros2 topic pub /voice_commands std_msgs/String "data: 'Go to the kitchen'"
```

### Example 2: Complete Voice-Controlled Navigation

This example shows a complete implementation of voice-controlled navigation:

```python
#!/usr/bin/env python3
# voice_navigation_demo.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import time

class VoiceNavigationDemo(Node):
    def __init__(self):
        super().__init__('voice_navigation_demo')

        # Publisher for voice commands
        self.voice_cmd_pub = self.create_publisher(String, '/voice_commands', 10)

        # Publisher for navigation goals (for verification)
        self.nav_goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # Timer for demo sequence
        self.demo_timer = self.create_timer(5.0, self.run_demo_sequence)
        self.demo_step = 0

        self.locations = [
            {'name': 'kitchen', 'x': 5.0, 'y': 3.0, 'command': 'Go to the kitchen'},
            {'name': 'living room', 'x': 0.0, 'y': 0.0, 'command': 'Go to the living room'},
            {'name': 'bedroom', 'x': -3.0, 'y': 2.0, 'command': 'Go to the bedroom'}
        ]

        self.get_logger().info('Voice Navigation Demo initialized')

    def run_demo_sequence(self):
        """Run a sequence of voice navigation commands"""
        if self.demo_step < len(self.locations):
            location = self.locations[self.demo_step]

            # Publish voice command
            cmd_msg = String()
            cmd_msg.data = location['command']
            self.voice_cmd_pub.publish(cmd_msg)

            self.get_logger().info(f'Published voice command: {location["command"]}')

            self.demo_step += 1
        else:
            # Demo sequence complete
            self.get_logger().info('Demo sequence complete')
            self.demo_timer.cancel()

def main(args=None):
    rclpy.init(args=args)

    demo = VoiceNavigationDemo()

    try:
        rclpy.spin(demo)
    except KeyboardInterrupt:
        demo.get_logger().info('Demo interrupted by user')
    finally:
        demo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Example 3: Voice-Controlled Manipulation

This example demonstrates voice-controlled manipulation tasks:

```python
#!/usr/bin/env python3
# voice_manipulation_demo.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class VoiceManipulationDemo(Node):
    def __init__(self):
        super().__init__('voice_manipulation_demo')

        # Publisher for voice commands
        self.voice_cmd_pub = self.create_publisher(String, '/voice_commands', 10)

        # Timer for demo sequence
        self.demo_timer = self.create_timer(8.0, self.run_manipulation_demo)
        self.demo_step = 0

        self.manipulation_tasks = [
            'Pick up the red cup',
            'Place the cup on the table',
            'Grasp the blue bottle',
            'Take the book from the shelf'
        ]

        self.get_logger().info('Voice Manipulation Demo initialized')

    def run_manipulation_demo(self):
        """Run a sequence of voice manipulation commands"""
        if self.demo_step < len(self.manipulation_tasks):
            task = self.manipulation_tasks[self.demo_step]

            # Publish voice command
            cmd_msg = String()
            cmd_msg.data = task
            self.voice_cmd_pub.publish(cmd_msg)

            self.get_logger().info(f'Published manipulation command: {task}')

            self.demo_step += 1
        else:
            # Demo sequence complete
            self.get_logger().info('Manipulation demo sequence complete')
            self.demo_timer.cancel()

def main(args=None):
    rclpy.init(args=args)

    demo = VoiceManipulationDemo()

    try:
        rclpy.spin(demo)
    except KeyboardInterrupt:
        demo.get_logger().info('Manipulation demo interrupted by user')
    finally:
        demo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary and Next Steps

In this chapter, we've explored the fundamental concepts and implementation techniques for voice-to-action systems in humanoid robotics. Key concepts and techniques covered include:

### Key Concepts Mastered
- **OpenAI Whisper Integration**: Understanding Whisper's capabilities for robotics applications and its integration with robotic systems
- **Speech Recognition with Whisper**: Implementing high-quality speech-to-text transcription using Whisper models
- **Natural Language Understanding**: Implementing intent recognition and parameter extraction using LLMs with Whisper transcription
- **Command Mapping**: Creating systems that translate Whisper-transcribed voice commands to robot actions
- **Multi-Step Execution**: Handling complex commands that require multiple sequential actions
- **ROS 2 Integration**: Properly integrating Whisper-based voice systems with ROS 2 architecture
- **Context-Aware Processing**: Enhancing command understanding with situational context using Whisper transcription

### Technical Implementation Highlights
- Developed Whisper-based speech recognition pipelines optimized for robotics applications
- Created WhisperAudioPreprocessor for audio preprocessing specifically for Whisper models
- Implemented WhisperLLMIntentRecognizer for processing Whisper transcriptions with LLMs
- Created WhisperVoiceToActionNode for complete Whisper-to-action pipeline integration with ROS 2
- Implemented multi-step command execution for complex tasks using Whisper transcription
- Established proper ROS 2 node architecture for Whisper-based voice processing
- Created context-aware command understanding systems using Whisper output
- Developed practical examples for navigation and manipulation with Whisper integration

### Best Practices Established
- Used appropriate preprocessing techniques to handle robot environment noise
- Implemented fallback systems for robust operation
- Applied context-aware processing for better command understanding
- Established proper error handling and user feedback mechanisms
- Created modular architecture for easy maintenance and extension

### Advanced Considerations
For production voice-to-action systems, additional considerations include:

#### 1. Privacy and Security
- **Local Processing**: Maximizing local processing to protect user privacy
- **Data Encryption**: Encrypting voice data during transmission and storage
- **Access Control**: Implementing proper authentication for sensitive commands
- **Data Retention**: Establishing policies for voice data retention and deletion

#### 2. Robustness and Reliability
- **Noise Robustness**: Advanced noise cancellation for robot environments
- **Error Recovery**: Graceful handling of misrecognition and execution failures
- **Redundancy**: Backup systems for critical functionality
- **Testing**: Comprehensive testing with diverse speakers and environments

#### 3. User Experience
- **Response Time**: Minimizing latency for responsive interaction
- **Feedback Mechanisms**: Clear audio and visual feedback for command recognition
- **Learning**: Systems that adapt to user preferences and speaking patterns
- **Accessibility**: Support for users with different abilities and needs

### Next Steps

With the foundation of voice-to-action systems established, the next chapter will build upon these concepts by exploring Cognitive Planning with LLMs. We'll cover:

- **LLM Integration**: Deep integration of Large Language Models for high-level reasoning
- **Planning Algorithms**: Advanced planning techniques using LLM capabilities
- **Reasoning Systems**: Creating systems that can reason about complex tasks and environments
- **Decision Making**: Implementing sophisticated decision-making processes guided by LLMs
- **Knowledge Integration**: Connecting LLMs with robot knowledge bases and perception systems

The knowledge gained in this chapter provides the essential foundation for creating intelligent humanoid robots that can understand and respond to natural voice commands, setting the stage for more sophisticated cognitive capabilities in the subsequent chapters.

### Navigation
- **Previous**: [Module 4 Overview](./index)
- **Next**: [Chapter 2: Cognitive Planning with LLMs](./chapter2-cognitive-planning-llms)