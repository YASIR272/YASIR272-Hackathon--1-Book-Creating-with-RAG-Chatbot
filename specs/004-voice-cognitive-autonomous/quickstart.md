# Quickstart Guide: Module 4 – Voice-to-Action & Cognitive Planning (LLMs & Autonomous Humanoids)

**Date**: 2025-12-17
**Feature**: 004-voice-cognitive-autonomous
**Status**: Complete

## Overview

This quickstart guide provides a step-by-step introduction to the concepts covered in Module 4: Voice-to-Action systems, Cognitive Planning with Large Language Models (LLMs), and Autonomous Humanoid development. By following this guide, you'll learn how to integrate voice commands, LLM-based reasoning, and robot control to create intelligent humanoid behaviors.

## Prerequisites

Before starting this module, ensure you have:

- Completed Modules 1-3 (ROS 2 fundamentals, Isaac Sim, Isaac ROS VSLAM, Nav2)
- Access to a computer with internet connection
- Python 3.8+ installed
- ROS 2 Humble Hawksbill installed
- Basic familiarity with Large Language Models (LLMs)
- (Optional) Access to OpenAI API key for advanced examples

## Setting Up the Development Environment

### 1. Install Required Python Libraries

```bash
pip install openai langchain transformers torch speechrecognition
pip install opencv-python numpy scipy matplotlib
pip install ros2-interfaces rclpy
```

### 2. Set Up API Keys

Create a `.env` file in your project directory with the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Verify ROS 2 Installation

Test that ROS 2 is properly configured:

```bash
ros2 topic list
ros2 node list
```

## Basic Voice Command Processing

### Step 1: Set Up Voice Recognition

Create a simple voice command recognizer:

```python
import speech_recognition as sr
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class VoiceCommandProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def listen_for_command(self):
        """Listen for and transcribe a voice command"""
        with self.microphone as source:
            print("Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"Heard: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
```

### Step 2: Process Commands with LLM

Add LLM-based command interpretation:

```python
class LLMCommandInterpreter:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def interpret_command(self, command_text):
        """Use LLM to interpret natural language command and extract intent"""
        prompt = f"""
        Parse this robot command and extract the intent and parameters:
        Command: "{command_text}"

        Respond in JSON format with:
        {{
            "intent": "navigation | manipulation | information | other",
            "action": "specific action to perform",
            "parameters": {{"param1": "value1", ...}}
        }}

        Be concise and accurate. If unsure, respond with intent "other".
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        import json
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except:
            # Fallback if JSON parsing fails
            return {
                "intent": "other",
                "action": command_text,
                "parameters": {}
            }
```

## Cognitive Planning with LLMs

### Step 3: Create a Cognitive Planner

Implement high-level planning using LLMs:

```python
class CognitivePlanner:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_plan(self, goal_description, environment_state):
        """Generate a multi-step plan to achieve a goal"""
        prompt = f"""
        Create a step-by-step plan to achieve this goal:
        Goal: {goal_description}

        Current environment state: {environment_state}

        Return a JSON array of tasks in the format:
        [
            {{
                "task_id": "unique_id",
                "description": "what to do",
                "type": "navigation | manipulation | perception | communication",
                "parameters": {{"param1": "value1"}},
                "dependencies": ["task_id_1", "task_id_2"]  // tasks that must complete first
            }}
        ]

        Ensure the plan is feasible given the environment state.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        import json
        try:
            tasks = json.loads(response.choices[0].message.content)
            return tasks
        except:
            # Fallback plan
            return [{
                "task_id": "fallback_task",
                "description": "Navigate to goal location",
                "type": "navigation",
                "parameters": {},
                "dependencies": []
            }]
```

## Vision-Language-Action Integration

### Step 4: Implement VLA Coordination

Create a coordinator that manages vision, language, and action:

```python
class VLACoordinator:
    def __init__(self):
        self.voice_processor = VoiceCommandProcessor()
        self.llm_interpreter = LLMCommandInterpreter()
        self.cognitive_planner = CognitivePlanner()
        self.robot_controller = self.initialize_robot_controller()

    def initialize_robot_controller(self):
        """Initialize ROS 2 based robot controller"""
        import rclpy
        from rclpy.node import Node

        class RobotController(Node):
            def __init__(self):
                super().__init__('vla_robot_controller')
                # Initialize action clients, publishers, subscribers
                self.nav_client = None  # Navigation action client
                self.manipulation_client = None  # Manipulation action client
                self.perception_client = None  # Perception service client

            def execute_navigation_task(self, goal_pose):
                # Execute navigation task
                pass

            def execute_manipulation_task(self, grasp_pose):
                # Execute manipulation task
                pass

        rclpy.init()
        return RobotController()

    def execute_voice_command(self, command_text):
        """Execute a voice command end-to-end"""
        # Interpret the command
        interpreted = self.llm_interpreter.interpret_command(command_text)

        if interpreted['intent'] == 'navigation':
            # Create a navigation plan
            environment_state = self.get_environment_state()
            plan = self.cognitive_planner.create_plan(
                f"Go to {interpreted['parameters'].get('location', 'destination')}",
                environment_state
            )

            # Execute the plan
            for task in plan:
                self.execute_task(task)

        elif interpreted['intent'] == 'manipulation':
            # Handle manipulation commands
            environment_state = self.get_environment_state()
            plan = self.cognitive_planner.create_plan(
                f"Grasp {interpreted['parameters'].get('object', 'item')}",
                environment_state
            )

            for task in plan:
                self.execute_task(task)

    def get_environment_state(self):
        """Get current state of the environment from perception system"""
        # In practice, this would query perception services
        return {
            "objects": ["table", "chair", "cup"],
            "robot_position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "navigation_goals": ["kitchen", "living_room", "bedroom"]
        }

    def execute_task(self, task):
        """Execute a single task based on its type"""
        if task['type'] == 'navigation':
            self.robot_controller.execute_navigation_task(task['parameters'])
        elif task['type'] == 'manipulation':
            self.robot_controller.execute_manipulation_task(task['parameters'])
        elif task['type'] == 'perception':
            # Execute perception task
            pass
        # Add more task types as needed
```

## Autonomous Humanoid Capstone Example

### Step 5: Complete Example

Here's a complete example that demonstrates the integration:

```python
def main():
    """Main example demonstrating VLA integration"""
    print("Starting VLA (Vision-Language-Action) demonstration...")

    # Initialize the VLA coordinator
    vla_system = VLACoordinator()

    # Example: Have the robot go to kitchen and pick up a cup
    command = "Please go to the kitchen and bring me a cup"

    print(f"Processing command: {command}")
    vla_system.execute_voice_command(command)

    print("Command execution completed!")

if __name__ == "__main__":
    main()
```

## Running the Examples

### 1. Test Voice Recognition (without ROS)

```bash
python -c "
from quickstart_example import VoiceCommandProcessor
processor = VoiceCommandProcessor()
command = processor.listen_for_command()
print(f'Command received: {command}')
"
```

### 2. Test LLM Interpretation

```bash
python -c "
from quickstart_example import LLMCommandInterpreter
interpreter = LLMCommandInterpreter()
result = interpreter.interpret_command('Go to the kitchen')
print(result)
"
```

### 3. Test Cognitive Planning

```bash
python -c "
from quickstart_example import CognitivePlanner
planner = CognitivePlanner()
plan = planner.create_plan('Navigate to the living room', {'objects': ['sofa', 'table']})
print(plan)
"
```

## Key Concepts Demonstrated

1. **Voice Command Processing**: Converting natural language to structured commands
2. **LLM Integration**: Using large language models for intent recognition and planning
3. **Cognitive Planning**: Breaking high-level goals into executable tasks
4. **VLA Coordination**: Integrating vision, language, and action systems
5. **ROS 2 Integration**: Connecting AI systems with robot control

## Next Steps

After completing this quickstart:

1. Review Chapter 1: Voice-to-Action systems for detailed implementation
2. Study Chapter 2: Cognitive Planning with LLMs for advanced reasoning techniques
3. Explore Chapter 3: Autonomous Humanoid capstone for complete integration examples
4. Experiment with different LLM models and parameters
5. Extend the examples to work with your specific robot platform

## Troubleshooting

### Common Issues

1. **Speech Recognition Fails**: Check microphone permissions and ambient noise levels
2. **LLM Requests Timeout**: Verify API key and internet connectivity
3. **ROS 2 Connection Issues**: Ensure ROS 2 environment is properly sourced
4. **Plan Generation Poor Quality**: Try adjusting LLM temperature or prompt engineering

### Performance Tips

- Use local LLMs for faster response times in development
- Cache frequently used plans for efficiency
- Implement proper error handling and fallback behaviors
- Monitor system resources during execution