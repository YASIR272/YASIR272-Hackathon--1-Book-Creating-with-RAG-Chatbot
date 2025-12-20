---
sidebar_position: 3
---

# Chapter 2: Cognitive Planning with LLMs

This chapter covers LLM integration for robotic planning, reasoning and decision-making, hierarchical task planning, and integration with robot execution systems for humanoid robots.

## Learning Objectives

- Understand how Large Language Models (LLMs) can be integrated into robotic planning systems
- Implement reasoning and decision-making processes using LLMs for humanoid robots
- Design hierarchical task planning systems that leverage LLM capabilities
- Integrate LLM-generated plans with robot execution systems for humanoid control
- Create practical examples demonstrating LLM-based planning for humanoid tasks
- Apply concept-first explanations following accessibility principles
- Ensure content focuses on LLM-based planning while excluding non-LLM topics
- Develop learning objectives and summary sections for effective education

## Table of Contents

1. [Introduction to Cognitive Planning with LLMs](#introduction-to-cognitive-planning-with-llms)
2. [LLM Integration for Robotic Planning](#llm-integration-for-robotic-planning)
3. [Reasoning and Decision-Making](#reasoning-and-decision-making)
4. [Hierarchical Task Planning](#hierarchical-task-planning)
5. [Integration with Robot Execution Systems](#integration-with-robot-execution-systems)
6. [Practical Examples](#practical-examples)
7. [Summary and Next Steps](#summary-and-next-steps)

## Conceptual Overview

Before diving into the technical implementation, it's important to understand the fundamental concepts behind cognitive planning with Large Language Models for humanoid robotics:

- **Cognitive Planning**: The process of using high-level reasoning to decompose complex tasks into executable actions for humanoid robots
- **Large Language Models (LLMs)**: Advanced AI models that can understand and generate human language, enabling natural task specification and reasoning
- **Robotic Planning Integration**: The process of connecting LLM outputs to robot control systems for physical execution
- **Hierarchical Task Decomposition**: Breaking down high-level goals into increasingly specific subtasks and primitive actions
- **Reasoning Systems**: AI systems that can make logical inferences and decisions based on environmental context and task requirements
- **Decision-Making Under Uncertainty**: Making intelligent choices when information is incomplete or uncertain
- **Knowledge Representation**: Structuring information in ways that LLMs can effectively use for planning and reasoning

These concepts form the foundation of LLM-based cognitive planning for humanoid robots, enabling robots to understand high-level goals and translate them into detailed execution plans.

## Introduction to Cognitive Planning with LLMs

Cognitive planning represents a paradigm shift in robotics, moving from traditional algorithmic planning to AI-driven reasoning that can handle complex, ambiguous, and high-level task specifications. For humanoid robots, cognitive planning is particularly valuable because it allows for natural task specification using everyday language rather than requiring detailed, low-level programming.

### The Evolution of Robotic Planning

Traditional robotic planning systems rely on formal mathematical models and deterministic algorithms to generate action sequences. While effective for well-structured tasks, these systems struggle with high-level, ambiguous, or complex tasks that require common sense reasoning and contextual understanding.

Cognitive planning with LLMs addresses these limitations by leveraging the natural language understanding and reasoning capabilities of large language models. This enables robots to:

- Interpret high-level task descriptions like "Clean the room" or "Help me find my keys"
- Apply common sense reasoning to fill in missing details
- Adapt plans based on environmental context and constraints
- Handle unexpected situations through flexible reasoning
- Learn from experience and improve planning over time

### LLM-Based Planning Architecture

The architecture for LLM-based cognitive planning typically follows this pattern:

```
High-Level Task → LLM Reasoning → Task Decomposition → Action Sequencing → Robot Execution
```

Each stage leverages the unique capabilities of LLMs while connecting to traditional robotics systems for execution.

### Applications in Humanoid Robotics

Humanoid robots benefit significantly from cognitive planning because:

- **Natural Interaction**: Users can specify tasks using natural language
- **Complex Tasks**: Humanoid robots perform complex, multi-step tasks that benefit from high-level reasoning
- **Adaptability**: LLMs can adapt plans to new situations and environments
- **Context Awareness**: LLMs can incorporate environmental and social context into planning
- **Learning Capability**: Systems can improve through interaction and experience

## LLM Integration for Robotic Planning

### Selecting Appropriate LLMs for Robotics

Different LLMs have different strengths for robotic planning applications. The choice depends on factors like response time, reasoning capability, cost, and deployment requirements.

#### OpenAI Models

OpenAI's GPT models are popular for robotic planning due to their strong reasoning capabilities and reliable API:

```python
import openai
import os
import json
import time
from typing import Dict, List, Any, Optional

class LLMPlanner:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize LLM-based planner with OpenAI models

        Args:
            api_key: OpenAI API key
            model: Model to use ('gpt-4', 'gpt-3.5-turbo', etc.)
        """
        openai.api_key = api_key
        self.model = model
        self.context_window = 8192 if "gpt-4" in model else 4096

    def plan_task(self, task_description: str, environment_state: Dict[str, Any]) -> Optional[Dict]:
        """
        Plan a task using LLM reasoning

        Args:
            task_description: High-level task description
            environment_state: Current state of the environment

        Returns:
            Task plan as dictionary or None if planning failed
        """
        prompt = self.create_planning_prompt(task_description, environment_state)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent planning
                max_tokens=1000,
                timeout=30
            )

            # Extract plan from response
            plan_text = response.choices[0].message.content

            # Parse the plan (assuming it's in JSON format)
            plan = self.parse_plan_response(plan_text)
            return plan

        except Exception as e:
            print(f"LLM planning failed: {e}")
            return None

    def create_planning_prompt(self, task_description: str, environment_state: Dict[str, Any]) -> str:
        """Create a detailed prompt for task planning"""
        return f"""
        Task: {task_description}

        Environment State: {json.dumps(environment_state, indent=2)}

        Generate a detailed plan to accomplish this task. Consider the following:
        1. Available objects and their locations
        2. Robot capabilities and limitations
        3. Safety constraints
        4. Efficiency considerations
        5. Potential obstacles or challenges

        Return in JSON format:
        {{
            "task_id": "unique identifier",
            "description": "Brief description of the plan",
            "tasks": [
                {{
                    "id": "task-001",
                    "description": "What to do",
                    "type": "navigation | manipulation | perception | communication",
                    "parameters": {{"param1": "value1"}},
                    "dependencies": ["task-id-1", "task-id-2"],  // Tasks that must complete first
                    "estimated_duration": 30  // Estimated time in seconds
                }}
            ],
            "estimated_total_duration": 300  // Total estimated time in seconds
        }}

        Be specific about locations, objects, and actions. Ensure the plan is executable by a humanoid robot.
        """

    def get_system_prompt(self) -> str:
        """System prompt defining the LLM's role"""
        return """
        You are an expert robotic task planner for humanoid robots. Your job is to decompose high-level tasks into detailed, executable action plans for humanoid robots.

        When creating plans:
        - Consider humanoid robot capabilities (bipedal locomotion, manipulation, perception)
        - Include navigation, manipulation, and perception tasks as needed
        - Account for safety and efficiency
        - Create detailed, specific instructions that can be executed by a robot
        - Ensure tasks are sequenced logically with proper dependencies
        - Include error handling and fallback behaviors where appropriate
        """

    def parse_plan_response(self, response_text: str) -> Optional[Dict]:
        """Parse the LLM response to extract the plan"""
        try:
            # Look for JSON in the response (in case there's additional text)
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # If JSON parsing fails, return None
        return None

    def refine_plan(self, original_plan: Dict, feedback: str) -> Optional[Dict]:
        """Refine an existing plan based on feedback"""
        prompt = f"""
        Original Plan:
        {json.dumps(original_plan, indent=2)}

        Feedback:
        {feedback}

        Refine the plan based on the feedback. Consider:
        1. Safety improvements
        2. Efficiency gains
        3. Better task sequencing
        4. Execution monitoring
        5. Environmental constraints mentioned in feedback

        Return the refined plan in the same JSON format.
        """

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            refined_plan_text = response.choices[0].message.content
            return self.parse_plan_response(refined_plan_text)

        except Exception as e:
            print(f"Plan refinement failed: {e}")
            return original_plan  # Return original if refinement fails
```

#### Open-Source LLM Integration

For deployment scenarios where API costs or privacy are concerns, open-source models can be used:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LocalLLMPlanner:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """
        Initialize local LLM planner using Hugging Face models

        Args:
            model_name: Name of the model to load
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Add pad token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def plan_task_local(self, task_description: str, environment_state: Dict[str, Any]) -> Optional[Dict]:
        """Plan task using local LLM"""
        prompt = self.create_planning_prompt(task_description, environment_state)

        # Tokenize input
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=len(inputs[0]) + 200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract plan from response
        plan = self.parse_plan_response(response[len(prompt):])
        return plan
```

### Planning with Environmental Context

Effective cognitive planning requires incorporating environmental context to make informed decisions:

```python
class ContextAwarePlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.knowledge_base = KnowledgeBase()
        self.context_memory = ContextMemory()

    def plan_with_context(self, task_description: str, robot_capabilities: Dict[str, Any]) -> Optional[Dict]:
        """Plan task considering environmental context and robot capabilities"""

        # Gather environmental context
        environment_state = self.gather_environmental_context()

        # Augment with robot capabilities
        full_context = {
            **environment_state,
            "robot_capabilities": robot_capabilities,
            "previous_experience": self.context_memory.get_recent_plans(task_description)
        }

        # Plan with full context
        plan = self.llm_planner.plan_task(task_description, full_context)

        if plan and self.validate_plan_against_capabilities(plan, robot_capabilities):
            return plan
        else:
            return self.generate_fallback_plan(task_description, robot_capabilities)

    def gather_environmental_context(self) -> Dict[str, Any]:
        """Gather current environmental context for planning"""
        context = {
            "current_location": self.get_current_location(),
            "visible_objects": self.get_visible_objects(),
            "navigation_map": self.get_navigation_map(),
            "time_of_day": self.get_time_of_day(),
            "known_entities": self.knowledge_base.get_known_entities(),
            "recent_events": self.context_memory.get_recent_events(5)
        }
        return context

    def validate_plan_against_capabilities(self, plan: Dict, capabilities: Dict[str, Any]) -> bool:
        """Validate that the plan is executable with given robot capabilities"""
        for task in plan.get("tasks", []):
            task_type = task.get("action_type", "")

            if task_type == "navigation":
                # Check if navigation capabilities are sufficient
                max_range = capabilities.get("navigation", {}).get("max_range", 0)
                if self.estimate_navigation_distance(task) > max_range:
                    return False

            elif task_type == "manipulation":
                # Check if manipulation capabilities are sufficient
                required_dof = task.get("parameters", {}).get("degrees_of_freedom", 0)
                available_dof = capabilities.get("manipulation", {}).get("degrees_of_freedom", 0)
                if required_dof > available_dof:
                    return False

        return True

    def estimate_navigation_distance(self, task: Dict) -> float:
        """Estimate navigation distance for a task"""
        # Implementation would calculate distance based on destination
        return 1.0  # Placeholder

    def get_current_location(self) -> Dict[str, float]:
        """Get current robot location"""
        # This would interface with localization system
        return {"x": 0.0, "y": 0.0, "theta": 0.0}

    def get_visible_objects(self) -> List[Dict[str, Any]]:
        """Get objects currently visible to the robot"""
        # This would interface with perception system
        return []

    def get_navigation_map(self) -> Dict[str, Any]:
        """Get current navigation map"""
        # This would interface with mapping system
        return {}

    def get_time_of_day(self) -> str:
        """Get current time of day"""
        import datetime
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"

    def generate_fallback_plan(self, task_description: str, capabilities: Dict[str, Any]) -> Optional[Dict]:
        """Generate a simple fallback plan when detailed planning fails"""
        return {
            "task_id": "fallback_plan",
            "description": f"Fallback plan for: {task_description}",
            "tasks": [
                {
                    "id": "fallback_001",
                    "description": "Request clarification for task",
                    "type": "communication",
                    "parameters": {"message": f"I need more information to perform: {task_description}"},
                    "dependencies": [],
                    "estimated_duration": 10
                }
            ],
            "estimated_total_duration": 10
        }
```

## Reasoning and Decision-Making

### Logical Reasoning for Task Planning

LLMs excel at logical reasoning, which can be leveraged for sophisticated task planning:

```python
class ReasoningEngine:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner

    def perform_causal_reasoning(self, situation: str, goal: str) -> List[str]:
        """Perform causal reasoning to understand how to achieve a goal"""
        prompt = f"""
        Situation: {situation}
        Goal: {goal}

        Perform causal reasoning to determine what needs to happen to achieve the goal.
        Consider:
        1. What conditions must be met
        2. What actions lead to the goal
        3. What obstacles might prevent success
        4. What resources are needed

        Return a list of necessary conditions and actions.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a logical reasoning expert. Analyze the causal relationships between situations and goals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            # Parse the response to extract reasoning steps
            reasoning_text = response.choices[0].message.content
            return self.parse_reasoning_steps(reasoning_text)

        except Exception as e:
            print(f"Causal reasoning failed: {e}")
            return []

    def perform_spatial_reasoning(self, environment: Dict[str, Any], task: str) -> Dict[str, Any]:
        """Perform spatial reasoning for navigation and manipulation tasks"""
        prompt = f"""
        Environment: {json.dumps(environment, indent=2)}
        Task: {task}

        Perform spatial reasoning to understand:
        1. Spatial relationships between objects
        2. Feasible paths for navigation
        3. Reachable locations for manipulation
        4. Spatial constraints and obstacles

        Return a JSON object with spatial analysis results.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a spatial reasoning expert. Analyze spatial relationships and constraints in the environment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            spatial_analysis = response.choices[0].message.content
            return self.parse_spatial_analysis(spatial_analysis)

        except Exception as e:
            print(f"Spatial reasoning failed: {e}")
            return {}

    def perform_temporal_reasoning(self, task_sequence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform temporal reasoning to optimize task scheduling"""
        prompt = f"""
        Task Sequence: {json.dumps(task_sequence, indent=2)}

        Perform temporal reasoning to:
        1. Optimize task ordering for efficiency
        2. Identify tasks that can be executed in parallel
        3. Determine critical path for longest-duration tasks
        4. Schedule tasks to minimize total execution time

        Return an optimized schedule with timing information.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a temporal reasoning expert. Optimize task scheduling and timing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            schedule = response.choices[0].message.content
            return self.parse_schedule(schedule)

        except Exception as e:
            print(f"Temporal reasoning failed: {e}")
            return {"optimized_sequence": task_sequence, "estimated_duration": sum(t.get("estimated_duration", 30) for t in task_sequence)}
```

### Decision-Making Under Uncertainty

Robots often operate in uncertain environments, requiring decision-making frameworks that can handle incomplete information:

```python
class UncertaintyAwareDecisionMaker:
    def __init__(self, reasoning_engine: ReasoningEngine):
        self.reasoning_engine = reasoning_engine
        self.uncertainty_models = self.initialize_uncertainty_models()

    def make_decision_under_uncertainty(self, options: List[Dict[str, Any]],
                                      environment_state: Dict[str, Any]) -> Dict[str, Any]:
        """Make decisions when faced with uncertainty"""

        # Evaluate each option considering uncertainty
        evaluations = []
        for option in options:
            evaluation = self.evaluate_option_uncertainty(option, environment_state)
            evaluations.append({
                "option": option,
                "evaluation": evaluation
            })

        # Select best option based on expected utility
        best_option = self.select_best_option(evaluations)
        return best_option

    def evaluate_option_uncertainty(self, option: Dict[str, Any],
                                  environment_state: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate an option considering various uncertainties"""

        # Factors to consider:
        # - Success probability
        # - Potential negative consequences
        # - Resource consumption
        # - Time requirements
        # - Impact on other tasks

        prompt = f"""
        Option: {json.dumps(option, indent=2)}
        Environment State: {json.dumps(environment_state, indent=2)}

        Evaluate this option considering uncertainties:
        1. Probability of success
        2. Potential negative outcomes
        3. Resource requirements
        4. Time commitment
        5. Impact on other objectives

        Return a JSON object with probabilities and estimates.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a decision analysis expert. Evaluate options under uncertainty."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            evaluation = response.choices[0].message.content
            return self.parse_evaluation(evaluation)

        except Exception as e:
            print(f"Option evaluation failed: {e}")
            # Return default evaluation
            return {
                "success_probability": 0.7,
                "negative_impact_probability": 0.1,
                "resource_usage": 0.5,
                "time_requirement": 1.0
            }

    def select_best_option(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best option using expected utility theory"""

        best_expected_utility = float('-inf')
        best_option = None

        for eval_item in evaluations:
            option = eval_item["option"]
            eval_results = eval_item["evaluation"]

            # Calculate expected utility
            success_prob = eval_results.get("success_probability", 0.5)
            negative_prob = eval_results.get("negative_impact_probability", 0.1)
            resource_usage = eval_results.get("resource_usage", 0.5)
            time_req = eval_results.get("time_requirement", 1.0)

            # Simple utility calculation (in practice, this would be more sophisticated)
            utility = (success_prob * 10.0 -
                      negative_prob * 5.0 -
                      resource_usage * 2.0 -
                      time_req * 0.5)

            if utility > best_expected_utility:
                best_expected_utility = utility
                best_option = option

        return {
            "selected_option": best_option,
            "expected_utility": best_expected_utility,
            "confidence": "high" if best_expected_utility > 5.0 else "medium" if best_expected_utility > 0.0 else "low"
        }

    def handle_partial_observation(self, belief_state: Dict[str, Any],
                                 action: Dict[str, Any]) -> Dict[str, Any]:
        """Update belief state when only partial observations are available"""

        # Use LLM to infer likely state changes given partial observation
        prompt = f"""
        Current Belief State: {json.dumps(belief_state, indent=2)}
        Action Taken: {json.dumps(action, indent=2)}
        Partial Observation: [Observation would be provided here]

        Given the action and partial observation, update the belief state.
        Consider:
        1. What is confirmed by the observation
        2. What remains uncertain
        3. How the action likely affected the state
        4. What can be inferred probabilistically

        Return updated belief state with uncertainty estimates.
        """

        # In practice, this would be called with actual observations
        pass
```

### Commonsense Reasoning Integration

Commonsense reasoning allows robots to make intuitive decisions based on general world knowledge:

```python
class CommonsenseReasoning:
    def __init__(self):
        self.common_knowledge = self.load_common_knowledge()

    def load_common_knowledge(self) -> Dict[str, Any]:
        """Load common knowledge that LLMs might not know or might get wrong"""
        return {
            "object_affordances": {
                "cup": ["contain_liquid", "graspable", "movable"],
                "chair": ["sittable", "movable", "support_surface"],
                "door": ["passable_when_open", "openable", "closeable"],
                "table": ["support_surface", "movable"]
            },
            "spatial_relations": {
                "kitchen": ["cooking", "food_storage", "eating"],
                "bedroom": ["sleeping", "resting", "clothing_storage"],
                "living_room": ["socializing", "entertainment", "resting"]
            },
            "temporal_patterns": {
                "morning": ["breakfast", "leaving_home", "exercise"],
                "evening": ["dinner", "relaxing", "returning_home"]
            }
        }

    def apply_commonsense_reasoning(self, task: str, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Apply commonsense reasoning to interpret and plan a task"""

        prompt = f"""
        Task: {task}
        Environment: {json.dumps(environment, indent=2)}
        Common Knowledge: {json.dumps(self.common_knowledge, indent=2)}

        Apply commonsense reasoning to:
        1. Interpret the task in the context of common knowledge
        2. Identify implicit requirements
        3. Consider typical sequences of actions
        4. Account for common-sense constraints

        Return a refined task interpretation with commonsense considerations.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a commonsense reasoning expert. Apply general world knowledge to interpret tasks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            refined_task = response.choices[0].message.content
            return self.parse_refined_task(refined_task)

        except Exception as e:
            print(f"Commonsense reasoning failed: {e}")
            return {"original_task": task, "commonsense_adjustments": []}

    def validate_plan_commonsense(self, plan: Dict[str, Any],
                                environment: Dict[str, Any]) -> List[str]:
        """Validate a plan using commonsense reasoning"""
        issues = []

        # Check for commonsense violations
        for task in plan.get("tasks", []):
            task_type = task.get("type", "")
            task_desc = task.get("description", "")

            # Example checks
            if "go to" in task_desc.lower() and task_type == "manipulation":
                issues.append(f"Task '{task_desc}' mixes navigation with manipulation inappropriately")

            # Check if task makes sense in current environment
            if self.check_environmental_consistency(task, environment):
                issues.append(f"Task '{task_desc}' is inconsistent with environment")

        return issues

    def check_environmental_consistency(self, task: Dict[str, Any],
                                      environment: Dict[str, Any]) -> bool:
        """Check if a task is consistent with the environment"""
        # Implementation would check for consistency
        return False  # Placeholder
```

## Hierarchical Task Planning

### Multi-Level Task Decomposition

Hierarchical planning breaks down complex tasks into manageable subtasks at different levels of abstraction:

```python
class HierarchicalPlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.task_hierarchy = TaskHierarchy()

    def create_hierarchical_plan(self, high_level_task: str,
                               environment_state: Dict[str, Any]) -> Optional[Dict]:
        """Create a hierarchical plan decomposing high-level tasks"""

        # Level 1: High-level task decomposition
        level_1_plan = self.decompose_high_level_task(high_level_task, environment_state)

        if not level_1_plan:
            return None

        # Level 2: Mid-level task refinement
        level_2_plan = self.refine_mid_level_tasks(level_1_plan, environment_state)

        # Level 3: Low-level action generation
        level_3_plan = self.generate_primitive_actions(level_2_plan, environment_state)

        # Integrate all levels
        hierarchical_plan = {
            "high_level_task": high_level_task,
            "level_1": level_1_plan,
            "level_2": level_2_plan,
            "level_3": level_3_plan,
            "dependencies": self.calculate_dependencies(level_3_plan),
            "estimated_duration": self.calculate_total_duration(level_3_plan)
        }

        return hierarchical_plan

    def decompose_high_level_task(self, task: str, env_state: Dict[str, Any]) -> Optional[Dict]:
        """Decompose high-level task into major subtasks"""
        prompt = f"""
        High-level Task: {task}
        Environment State: {json.dumps(env_state, indent=2)}

        Decompose this high-level task into 3-7 major subtasks that represent the main phases of accomplishing the goal.
        Each subtask should be:
        1. Meaningful and substantial
        2. Logically ordered
        3. Cover all aspects of the main task

        Return in JSON format:
        {{
            "subtasks": [
                {{"id": "ht001", "description": "Major subtask 1", "type": "logical_category"}},
                {{"id": "ht002", "description": "Major subtask 2", "type": "logical_category"}}
            ]
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a task decomposition expert. Break down high-level tasks into major subtasks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            result = response.choices[0].message.content
            return self.parse_json_response(result)

        except Exception as e:
            print(f"High-level decomposition failed: {e}")
            return None

    def refine_mid_level_tasks(self, level_1_plan: Dict, env_state: Dict[str, Any]) -> Optional[Dict]:
        """Refine high-level subtasks into mid-level tasks"""
        mid_level_tasks = []

        for high_task in level_1_plan.get("subtasks", []):
            refined_tasks = self.refine_single_task(high_task, env_state)
            mid_level_tasks.extend(refined_tasks)

        return {"tasks": mid_level_tasks}

    def refine_single_task(self, task: Dict, env_state: Dict[str, Any]) -> List[Dict]:
        """Refine a single task into more specific subtasks"""
        prompt = f"""
        Task: {task['description']}
        Environment State: {json.dumps(env_state, indent=2)}

        Break down this task into 2-5 more specific subtasks that detail how to accomplish it.
        Each subtask should be more specific than the parent task.

        Return in JSON format:
        {{
            "subtasks": [
                {{"id": "mt001", "description": "More specific subtask", "parent_id": "{task['id']}", "type": "action_category"}},
                {{"id": "mt002", "description": "More specific subtask", "parent_id": "{task['id']}", "type": "action_category"}}
            ]
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a task refinement expert. Break down tasks into more specific subtasks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            result = response.choices[0].message.content
            parsed = self.parse_json_response(result)
            return parsed.get("subtasks", [])

        except Exception as e:
            print(f"Mid-level refinement failed for task {task['id']}: {e}")
            # Return a basic refinement
            return [{"id": f"{task['id']}_impl", "description": f"Implement {task['description']}", "parent_id": task['id'], "type": "implementation"}]

    def generate_primitive_actions(self, level_2_plan: Dict, env_state: Dict[str, Any]) -> Optional[Dict]:
        """Generate primitive actions from mid-level tasks"""
        primitive_tasks = []

        for mid_task in level_2_plan.get("tasks", []):
            primitives = self.generate_primitives_for_task(mid_task, env_state)
            primitive_tasks.extend(primitives)

        return {"tasks": primitive_tasks}

    def generate_primitives_for_task(self, task: Dict, env_state: Dict[str, Any]) -> List[Dict]:
        """Generate primitive robot actions for a specific task"""
        prompt = f"""
        Task: {task['description']}
        Environment State: {json.dumps(env_state, indent=2)}

        Generate 1-5 primitive robot actions that would accomplish this task.
        Each action should be:
        1. A specific robot behavior (navigation, manipulation, perception, etc.)
        2. Executable by a humanoid robot
        3. Include specific parameters where needed

        Return in JSON format:
        {{
            "actions": [
                {{"id": "pa001", "action_type": "navigation", "description": "Go to specific location", "parameters": {{"target_x": 1.0, "target_y": 2.0}}}},
                {{"id": "pa002", "action_type": "manipulation", "description": "Grasp object", "parameters": {{"object_id": "cup_01"}}}}
            ]
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a robot action generator. Create specific primitive actions for humanoid robots."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )

            result = response.choices[0].message.content
            parsed = self.parse_json_response(result)
            return parsed.get("actions", [])

        except Exception as e:
            print(f"Primitive generation failed for task {task['id']}: {e}")
            # Return a basic primitive
            return [{"id": f"{task['id']}_exec", "action_type": "generic", "description": f"Execute {task['description']}", "parameters": {}}]

    def calculate_dependencies(self, level_3_plan: Dict) -> Dict[str, List[str]]:
        """Calculate dependencies between primitive actions"""
        dependencies = {}

        # Simple dependency calculation based on task types and parameters
        tasks = level_3_plan.get("tasks", [])

        for i, task in enumerate(tasks):
            task_id = task.get("id", f"task_{i}")
            deps = []

            # Example dependency rules:
            # - Navigation must precede manipulation at destination
            # - Perception must precede actions requiring object information
            for j, other_task in enumerate(tasks):
                if i == j:
                    continue

                other_id = other_task.get("id", f"task_{j}")

                # Check for dependencies
                if self.tasks_depend_on_each_other(task, other_task):
                    deps.append(other_id)

            dependencies[task_id] = deps

        return dependencies

    def tasks_depend_on_each_other(self, task1: Dict, task2: Dict) -> bool:
        """Check if two tasks have dependencies"""
        # Example dependency rules
        # If task1 is navigation and task2 is manipulation at same location, task2 depends on task1
        if (task1.get("action_type") == "navigation" and
            task2.get("action_type") == "manipulation" and
            self.navigation_provides_access_for_manipulation(task1, task2)):
            return True

        # If task1 is perception and task2 requires the perceived information
        if (task1.get("action_type") == "perception" and
            task2.get("requires_perception") and
            task1.get("perceives_object") == task2.get("target_object")):
            return True

        return False

    def navigation_provides_access_for_manipulation(self, nav_task: Dict, manip_task: Dict) -> bool:
        """Check if navigation task provides access for manipulation task"""
        # Implementation would compare locations
        return True  # Placeholder
```

### Plan Refinement and Adaptation

Plans need to be refined and adapted as the robot executes them and encounters new information:

```python
class PlanRefiner:
    def __init__(self, hierarchical_planner: HierarchicalPlanner):
        self.hierarchical_planner = hierarchical_planner

    def refine_plan_during_execution(self, current_plan: Dict, execution_feedback: Dict[str, Any]) -> Dict:
        """Refine plan based on execution feedback and new information"""

        # Analyze execution feedback
        completed_tasks = execution_feedback.get("completed_tasks", [])
        failed_tasks = execution_feedback.get("failed_tasks", [])
        new_information = execution_feedback.get("new_information", {})

        # Update environment state with new information
        updated_env_state = {
            **current_plan.get("environment_state", {}),
            **execution_feedback["new_information"]
        }

        # Identify tasks that need replanning due to failures or new information
        tasks_to_replan = self.identify_tasks_needing_replanning(
            current_plan, failed_tasks, new_information
        )

        # Regenerate affected parts of the plan
        refined_plan = self.regenerate_plan_parts(
            current_plan, tasks_to_replan, updated_env_state
        )

        # Revalidate the plan
        validated_plan = self.validate_plan(refined_plan, updated_env_state)

        return validated_plan

    def update_environment_state(self, current_state: Dict, new_info: Dict) -> Dict:
        """Update environment state with new information from execution"""
        updated_state = current_state.copy()

        # Update known objects, locations, etc.
        if "detected_objects" in new_info:
            updated_state["known_objects"] = new_info["detected_objects"]

        if "new_location" in new_info:
            updated_state["current_location"] = new_info["new_location"]

        if "obstacles" in new_info:
            updated_state["obstacles"] = new_info["obstacles"]

        return updated_state

    def identify_tasks_needing_replanning(self, current_plan: Dict,
                                        failed_tasks: List[Dict],
                                        new_information: Dict) -> List[str]:
        """Identify which tasks need replanning based on failures and new info"""
        tasks_to_replan = set()

        # Add failed tasks
        for failed_task in failed_tasks:
            tasks_to_replan.add(failed_task.get("task_id", ""))

        # Add tasks affected by new information
        if new_information.get("obstacle_detected"):
            # Find navigation tasks that go through the obstacle location
            for task in current_plan.get("level_3", {}).get("tasks", []):
                if (task.get("action_type") == "navigation" and
                    self.navigation_path_blocked(task, new_information)):
                    tasks_to_replan.add(task.get("id", ""))

        # Add tasks that depend on failed tasks
        dependencies = current_plan.get("dependencies", {})
        for failed_task_id in failed_tasks:
            for task_id, deps in dependencies.items():
                if failed_task_id in deps:
                    tasks_to_replan.add(task_id)

        return list(tasks_to_replan)

    def navigation_path_blocked(self, nav_task: Dict, new_info: Dict) -> bool:
        """Check if navigation path is blocked by new obstacle information"""
        # Implementation would check if task path intersects with new obstacles
        return False  # Placeholder

    def regenerate_plan_parts(self, current_plan: Dict, tasks_to_replan: List[str],
                            env_state: Dict) -> Dict:
        """Regenerate parts of the plan that need replanning"""
        # For now, return the original plan with failed tasks marked
        # In practice, this would intelligently regenerate affected parts
        updated_plan = current_plan.copy()

        # Mark failed tasks
        for task_id in tasks_to_replan:
            self.mark_task_failed(updated_plan, task_id)

        # Add recovery tasks
        recovery_tasks = self.generate_recovery_tasks(tasks_to_replan, env_state)
        updated_plan["recovery_tasks"] = recovery_tasks

        return updated_plan

    def mark_task_failed(self, plan: Dict, task_id: str):
        """Mark a task as failed in the plan"""
        # This would traverse the plan hierarchy to mark the task
        pass

    def generate_recovery_tasks(self, failed_task_ids: List[str], env_state: Dict) -> List[Dict]:
        """Generate recovery tasks for failed tasks"""
        recovery_tasks = []

        for failed_task_id in failed_task_ids:
            # Generate appropriate recovery action
            recovery_task = {
                "id": f"recovery_{failed_task_id}",
                "description": f"Recovery action for failed task {failed_task_id}",
                "action_type": "recovery",
                "parameters": {"original_task_id": failed_task_id},
                "estimated_duration": 30
            }
            recovery_tasks.append(recovery_task)

        return recovery_tasks

    def validate_plan(self, plan: Dict, env_state: Dict) -> Dict:
        """Validate that the plan is still feasible with current environment"""
        validation_result = {
            "is_valid": True,
            "issues": [],
            "suggestions": []
        }

        # Check if all required objects are still available
        required_objects = self.extract_required_objects(plan)
        available_objects = env_state.get("known_objects", [])

        for obj in required_objects:
            if obj not in available_objects:
                validation_result["is_valid"] = False
                validation_result["issues"].append(f"Required object not available: {obj}")

        # Check if navigation destinations are still accessible
        navigation_tasks = [t for t in plan.get("level_3", {}).get("tasks", [])
                           if t.get("action_type") == "navigation"]

        for nav_task in navigation_tasks:
            if not self.destination_accessible(nav_task, env_state):
                validation_result["is_valid"] = False
                validation_result["issues"].append(f"Destination not accessible: {nav_task.get('description', '')}")

        return {**plan, "validation": validation_result}

    def extract_required_objects(self, plan: Dict) -> List[str]:
        """Extract list of objects required by the plan"""
        objects = []

        for task in plan.get("level_3", {}).get("tasks", []):
            params = task.get("parameters", {})
            if "object_id" in params:
                objects.append(params["object_id"])
            if "target_object" in params:
                objects.append(params["target_object"])

        return list(set(objects))  # Remove duplicates

    def destination_accessible(self, nav_task: Dict, env_state: Dict) -> bool:
        """Check if navigation destination is accessible"""
        # Implementation would check navigation map and obstacles
        return True  # Placeholder
```

## Integration with Robot Execution Systems

### ROS 2 Integration for Plan Execution

The cognitive planning system needs to integrate with ROS 2 execution systems to control the humanoid robot:

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
from typing import Dict, Any, List, Optional

class PlanExecutionNode(Node):
    def __init__(self):
        super().__init__('plan_execution_node')

        # Initialize components
        self.hierarchical_planner = HierarchicalPlanner(LLMPlanner(os.getenv("OPENAI_API_KEY")))
        self.plan_refiner = PlanRefiner(self.hierarchical_planner)
        self.execution_monitor = ExecutionMonitor(self)

        # Publishers and subscribers
        self.status_pub = self.create_publisher(String, 'plan_status', 10)
        self.feedback_pub = self.create_publisher(String, 'execution_feedback', 10)
        self.command_pub = self.create_publisher(String, 'robot_commands', 10)

        # Service servers
        self.plan_service = self.create_service(
            PlanTask,
            'plan_task',
            self.plan_task_callback
        )

        self.execute_plan_service = self.create_service(
            ExecutePlan,
            'execute_plan',
            self.execute_plan_callback
        )

        # Action clients for robot capabilities
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.manip_client = ActionClient(self, ManipulateObject, 'manipulate_object')
        self.percept_client = ActionClient(self, SenseEnvironment, 'sense_environment')

        # Current execution state
        self.current_plan = None
        self.execution_active = False
        self.current_task_index = 0

        # Timer for plan execution
        self.execution_timer = self.create_timer(0.1, self.execution_loop)  # 10 Hz

        self.get_logger().info('Plan Execution Node initialized')

    def plan_task_callback(self, request, response):
        """Handle task planning requests"""
        try:
            # Get current environment state
            env_state = self.get_current_environment_state()

            # Create hierarchical plan
            plan = self.hierarchical_planner.create_hierarchical_plan(
                request.task_description,
                env_state
            )

            if plan:
                response.success = True
                response.plan_id = plan.get("plan_id", "unknown")
                response.plan_description = plan.get("high_level_task", "unknown")
                response.estimated_duration = plan.get("estimated_duration", 0)

                # Store plan for execution
                self.current_plan = plan
                self.get_logger().info(f'Plan created successfully: {plan.get("high_level_task")}')
            else:
                response.success = False
                response.error_message = "Failed to create plan"
                self.get_logger().error('Plan creation failed')

        except Exception as e:
            response.success = False
            response.error_message = f"Exception during planning: {str(e)}"
            self.get_logger().error(f'Planning exception: {e}')

        return response

    def execute_plan_callback(self, request, response):
        """Handle plan execution requests"""
        try:
            if not self.current_plan:
                response.success = False
                response.error_message = "No plan available for execution"
                return response

            # Start execution
            self.start_plan_execution(self.current_plan)

            response.success = True
            response.execution_id = f"exec_{int(time.time())}"
            response.status = "EXECUTING"

            self.get_logger().info('Plan execution started')

        except Exception as e:
            response.success = False
            response.error_message = f"Exception during execution: {str(e)}"
            self.get_logger().error(f'Execution exception: {e}')

        return response

    def start_plan_execution(self, plan: Dict):
        """Start executing a plan"""
        self.current_plan = plan
        self.execution_active = True
        self.current_task_index = 0
        self.get_logger().info(f'Starting execution of plan: {plan.get("high_level_task")}')

    def execution_loop(self):
        """Main execution loop"""
        if not self.execution_active or not self.current_plan:
            return

        # Get current task to execute
        current_task = self.get_current_task()
        if not current_task:
            # Plan completed
            self.plan_execution_completed()
            return

        # Execute the current task
        task_success = self.execute_single_task(current_task)

        if task_success:
            # Move to next task
            self.current_task_index += 1
            self.get_logger().info(f'Task completed, moving to next task ({self.current_task_index}/{len(self.get_plan_tasks())})')
        else:
            # Task failed - handle failure
            self.handle_task_failure(current_task)
            return

    def get_current_task(self) -> Optional[Dict]:
        """Get the current task to execute"""
        tasks = self.get_plan_tasks()
        if 0 <= self.current_task_index < len(tasks):
            return tasks[self.current_task_index]
        return None

    def get_plan_tasks(self) -> List[Dict]:
        """Get all tasks from the current plan"""
        if self.current_plan:
            return self.current_plan.get("level_3", {}).get("tasks", [])
        return []

    def execute_single_task(self, task: Dict) -> bool:
        """Execute a single task based on its type"""
        task_type = task.get("action_type", "")

        try:
            if task_type == "navigation":
                return self.execute_navigation_task(task)
            elif task_type == "manipulation":
                return self.execute_manipulation_task(task)
            elif task_type == "perception":
                return self.execute_perception_task(task)
            elif task_type == "communication":
                return self.execute_communication_task(task)
            else:
                return self.execute_generic_task(task)

        except Exception as e:
            self.get_logger().error(f'Task execution failed: {e}')
            return False

    def execute_navigation_task(self, task: Dict) -> bool:
        """Execute a navigation task"""
        try:
            # Extract navigation parameters
            target_x = task.get("parameters", {}).get("target_x", 0.0)
            target_y = task.get("parameters", {}).get("target_y", 0.0)

            # Create navigation goal
            goal_msg = NavigateToPose.Goal()
            goal_msg.pose.header.frame_id = "map"
            goal_msg.pose.pose.position.x = target_x
            goal_msg.pose.pose.position.y = target_y
            goal_msg.pose.pose.position.z = 0.0
            goal_msg.pose.pose.orientation.w = 1.0  # No rotation

            # Wait for action server
            if not self.nav_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error('Navigation action server not available')
                return False

            # Send goal
            future = self.nav_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, future)

            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error('Navigation goal rejected')
                return False

            # Get result
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)

            result = result_future.result()
            return result.status == GoalStatus.STATUS_SUCCEEDED

        except Exception as e:
            self.get_logger().error(f'Navigation task execution failed: {e}')
            return False

    def execute_manipulation_task(self, task: Dict) -> bool:
        """Execute a manipulation task"""
        try:
            # Extract manipulation parameters
            object_id = task.get("parameters", {}).get("object_id", "")
            action_type = task.get("parameters", {}).get("action_type", "grasp")

            # Create manipulation goal
            goal_msg = ManipulateObject.Goal()
            goal_msg.object_id = object_id
            goal_msg.action_type = action_type

            # Wait for action server
            if not self.manip_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error('Manipulation action server not available')
                return False

            # Send goal
            future = self.manip_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, future)

            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error('Manipulation goal rejected')
                return False

            # Get result
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)

            result = result_future.result()
            return result.status == GoalStatus.STATUS_SUCCEEDED

        except Exception as e:
            self.get_logger().error(f'Manipulation task execution failed: {e}')
            return False

    def execute_perception_task(self, task: Dict) -> bool:
        """Execute a perception task"""
        try:
            # Extract perception parameters
            object_type = task.get("parameters", {}).get("object_type", "any")
            search_area = task.get("parameters", {}).get("search_area", "current_view")

            # Create perception goal
            goal_msg = SenseEnvironment.Goal()
            goal_msg.object_type = object_type
            goal_msg.search_area = search_area

            # Wait for action server
            if not self.percept_client.wait_for_server(timeout_sec=5.0):
                self.get_logger().error('Perception action server not available')
                return False

            # Send goal
            future = self.percept_client.send_goal_async(goal_msg)
            rclpy.spin_until_future_complete(self, future)

            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error('Perception goal rejected')
                return False

            # Get result
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)

            result = result_future.result()
            return result.status == GoalStatus.STATUS_SUCCEEDED

        except Exception as e:
            self.get_logger().error(f'Perception task execution failed: {e}')
            return False

    def execute_communication_task(self, task: Dict) -> bool:
        """Execute a communication task"""
        try:
            message = task.get("parameters", {}).get("message", "")

            # Publish communication message
            comm_msg = String()
            comm_msg.data = message
            self.command_pub.publish(comm_msg)

            # For now, assume communication always succeeds
            return True

        except Exception as e:
            self.get_logger().error(f'Communication task execution failed: {e}')
            return False

    def execute_generic_task(self, task: Dict) -> bool:
        """Execute a generic task"""
        self.get_logger().warn(f'Executing generic task: {task.get("description", "unknown")}')
        # For generic tasks, we'll just log and assume success
        return True

    def handle_task_failure(self, failed_task: Dict):
        """Handle failure of a task during execution"""
        self.get_logger().error(f'Task failed: {failed_task.get("description", "unknown")}')

        # Generate feedback about the failure
        feedback = {
            "failed_task": failed_task,
            "failure_time": self.get_clock().now().to_msg(),
            "recovery_attempts": 0
        }

        # Attempt recovery
        recovery_success = self.attempt_task_recovery(failed_task)

        if not recovery_success:
            # If recovery fails, stop execution
            self.execution_active = False
            self.get_logger().error('Task recovery failed, stopping execution')
        else:
            self.get_logger().info('Task recovery successful, continuing execution')

    def attempt_task_recovery(self, failed_task: Dict) -> bool:
        """Attempt to recover from a failed task"""
        task_type = failed_task.get("action_type", "generic")

        if task_type == "navigation":
            return self.recover_navigation_failure(failed_task)
        elif task_type == "manipulation":
            return self.recover_manipulation_failure(failed_task)
        elif task_type == "perception":
            return self.recover_perception_failure(failed_task)
        else:
            # For other task types, try alternative approaches
            return self.try_alternative_approach(failed_task)

    def recover_navigation_failure(self, failed_task: Dict) -> bool:
        """Recover from navigation failure"""
        # Try alternative path
        # Retry with different parameters
        # Request human assistance
        return False  # Placeholder - implement actual recovery

    def recover_manipulation_failure(self, failed_task: Dict) -> bool:
        """Recover from manipulation failure"""
        # Adjust grasp parameters
        # Try different approach angle
        # Request repositioning
        return False  # Placeholder - implement actual recovery

    def recover_perception_failure(self, failed_task: Dict) -> bool:
        """Recover from perception failure"""
        # Change viewpoint
        # Adjust sensor parameters
        # Retry with different settings
        return False  # Placeholder - implement actual recovery

    def try_alternative_approach(self, failed_task: Dict) -> bool:
        """Try an alternative approach to complete the task"""
        # This would implement fallback strategies
        return False  # Placeholder

    def plan_execution_completed(self):
        """Handle completion of plan execution"""
        self.execution_active = False
        self.get_logger().info('Plan execution completed successfully')

        # Publish completion status
        status_msg = String()
        status_msg.data = f"PLAN_COMPLETED: {self.current_plan.get('high_level_task', 'unknown')}"
        self.status_pub.publish(status_msg)

    def get_current_environment_state(self) -> Dict[str, Any]:
        """Get current environment state from various sensors and systems"""
        # This would integrate with actual sensor data and robot systems
        return {
            "current_location": {"x": 0.0, "y": 0.0, "theta": 0.0},
            "known_objects": [],
            "navigation_map": {},
            "battery_level": 0.85,
            "robot_status": "operational"
        }

    def destroy_node(self):
        """Clean up resources"""
        if self.nav_client:
            self.nav_client.destroy()
        if self.manip_client:
            self.manip_client.destroy()
        if self.percept_client:
            self.percept_client.destroy()
        super().destroy_node()
```

## Practical Examples

### Example 1: Cognitive Planning for Room Cleaning

This example demonstrates how to create a cognitive plan for a complex task like cleaning a room:

```python
#!/usr/bin/env python3
# room_cleaning_demo.py

import json
import time

class RoomCleaningDemo:
    def __init__(self):
        self.planner = LLMPlanner(api_key=os.getenv("OPENAI_API_KEY"))
        self.context_aware_planner = ContextAwarePlanner(self.planner)

    def create_cleaning_plan(self):
        """Create a plan for cleaning a room"""
        task_description = "Clean the living room by picking up items and organizing the space"

        environment_state = {
            "room_layout": {
                "size": "4m x 5m",
                "furniture": ["sofa", "coffee_table", "tv_stand", "bookshelf"],
                "obstacles": []
            },
            "objects_to_clean": [
                {"name": "books", "location": "coffee_table", "count": 5},
                {"name": "cups", "location": "side_table", "count": 2},
                {"name": "papers", "location": "floor", "count": 8},
                {"name": "toys", "location": "carpet", "count": 3}
            ],
            "storage_locations": [
                {"type": "bookshelf", "capacity": "high", "accessible": True},
                {"type": "cabinet", "type": "closed", "accessible": True}
            ],
            "robot_capabilities": {
                "navigation": {"max_range": 10.0, "precision": "high"},
                "manipulation": {"max_weight": 2.0, "dof": 7},
                "perception": {"range": 5.0, "resolution": "high"}
            }
        }

        # Create the plan
        plan = self.context_aware_planner.plan_with_context(
            task_description,
            environment_state["robot_capabilities"]
        )

        if plan:
            print("Room cleaning plan created:")
            print(json.dumps(plan, indent=2))
            return plan
        else:
            print("Failed to create cleaning plan")
            return None

    def execute_cleaning_simulation(self, plan):
        """Simulate execution of the cleaning plan"""
        print("\nStarting room cleaning simulation...")

        for i, task in enumerate(plan.get("tasks", [])):
            print(f"\nStep {i+1}/{len(plan['tasks'])}: {task.get('description', 'Unknown task')}")

            # Simulate task execution
            estimated_duration = task.get("estimated_duration", 30)
            print(f"  Estimated duration: {estimated_duration}s")

            # Simulate execution time
            time.sleep(min(2, estimated_duration / 10))  # Faster simulation

            print(f"  Status: COMPLETED")

        print(f"\nRoom cleaning completed successfully!")
        print(f"Total estimated time: {plan.get('estimated_total_duration', 0)} seconds")

def main():
    demo = RoomCleaningDemo()

    print("Room Cleaning Cognitive Planning Demo")
    print("=" * 40)

    # Create the cleaning plan
    plan = demo.create_cleaning_plan()

    if plan:
        # Execute the plan (simulation)
        demo.execute_cleaning_simulation(plan)
    else:
        print("Demo failed - could not create plan")

if __name__ == "__main__":
    main()
```

### Example 2: Multi-Room Navigation and Task Planning

This example shows how to plan complex tasks across multiple rooms:

```python
#!/usr/bin/env python3
# multi_room_task_demo.py

class MultiRoomTaskDemo:
    def __init__(self):
        self.planner = LLMPlanner(api_key=os.getenv("OPENAI_API_KEY"))
        self.hierarchical_planner = HierarchicalPlanner(self.planner)

    def create_multi_room_plan(self):
        """Create a plan for tasks spanning multiple rooms"""
        task_description = "Go to the kitchen, bring ingredients to the dining room, set the table, then return to the living room"

        environment_state = {
            "building_layout": {
                "rooms": ["kitchen", "dining_room", "living_room"],
                "connections": [
                    {"from": "kitchen", "to": "dining_room", "distance": 3.0},
                    {"from": "dining_room", "to": "living_room", "distance": 4.0},
                    {"from": "kitchen", "to": "living_room", "distance": 8.0}
                ]
            },
            "available_ingredients": {
                "kitchen": ["flour", "eggs", "milk", "sugar", "butter"]
            },
            "dining_room_setup": {
                "table_size": "large",
                "chairs": 6,
                "available_space": "high"
            },
            "robot_capabilities": {
                "navigation": {"max_range": 15.0, "precision": "medium"},
                "manipulation": {"max_items": 3, "max_weight": 5.0, "dof": 7},
                "perception": {"range": 5.0, "resolution": "high"}
            }
        }

        # Create hierarchical plan
        plan = self.hierarchical_planner.create_hierarchical_plan(
            task_description,
            environment_state
        )

        if plan:
            print("Multi-room task plan created:")
            print(f"High-level task: {plan['high_level_task']}")
            print(f"Estimated duration: {plan['estimated_duration']} seconds")
            print(f"Level 1 tasks: {len(plan['level_1']['subtasks'])}")
            print(f"Level 2 tasks: {len(plan['level_2']['tasks'])}")
            print(f"Level 3 tasks: {len(plan['level_3']['tasks'])}")
            return plan
        else:
            print("Failed to create multi-room plan")
            return None

    def analyze_plan_efficiency(self, plan):
        """Analyze the efficiency of the created plan"""
        tasks = plan.get("level_3", {}).get("tasks", [])

        # Count different task types
        navigation_tasks = [t for t in tasks if t.get("action_type") == "navigation"]
        manipulation_tasks = [t for t in tasks if t.get("action_type") == "manipulation"]
        perception_tasks = [t for t in tasks if t.get("action_type") == "perception"]

        print(f"\nPlan Analysis:")
        print(f"- Total tasks: {len(tasks)}")
        print(f"- Navigation tasks: {len(navigation_tasks)}")
        print(f"- Manipulation tasks: {len(manipulation_tasks)}")
        print(f"- Perception tasks: {len(perception_tasks)}")

        # Calculate efficiency metrics
        total_distance = sum(
            self.estimate_navigation_distance(t)
            for t in navigation_tasks
        )

        print(f"- Estimated total navigation distance: {total_distance:.2f} meters")
        print(f"- Estimated total duration: {plan['estimated_duration']} seconds")

        # Suggest optimizations
        if len(navigation_tasks) > 5:
            print("- Suggestion: Consider task batching to reduce navigation")
        if total_distance > 20:
            print("- Suggestion: Optimize route for shorter travel distance")

def main():
    demo = MultiRoomTaskDemo()

    print("Multi-Room Task Planning Demo")
    print("=" * 30)

    # Create the multi-room plan
    plan = demo.create_multi_room_plan()

    if plan:
        # Analyze the plan
        demo.analyze_plan_efficiency(plan)
    else:
        print("Demo failed - could not create plan")

if __name__ == "__main__":
    main()
```

### Example 3: Adaptive Task Planning with Feedback

This example demonstrates how plans can be adapted based on execution feedback:

```python
#!/usr/bin/env python3
# adaptive_planning_demo.py

class AdaptivePlanningDemo:
    def __init__(self):
        self.planner = LLMPlanner(api_key=os.getenv("OPENAI_API_KEY"))
        self.refiner = PlanRefiner(
            HierarchicalPlanner(self.planner)
        )

    def create_original_plan(self):
        """Create an original plan for a task"""
        task_description = "Navigate to the office and retrieve the red folder from the desk"

        environment_state = {
            "robot_location": {"x": 0.0, "y": 0.0},
            "office_location": {"x": 5.0, "y": 3.0},
            "desk_location": {"x": 5.5, "y": 3.5},
            "known_objects": [
                {"name": "red_folder", "location": {"x": 5.5, "y": 3.5}, "type": "folder"}
            ],
            "robot_capabilities": {
                "navigation": {"max_range": 10.0, "precision": "high"},
                "manipulation": {"max_weight": 1.0, "dof": 7},
                "perception": {"range": 3.0, "resolution": "high"}
            }
        }

        plan = self.planner.plan_task(task_description, environment_state)
        return plan, environment_state

    def simulate_execution_with_obstacle(self, original_plan, original_env_state):
        """Simulate execution encountering an unexpected obstacle"""
        print("Original plan execution...")

        # Simulate reaching office but finding path to desk blocked
        execution_feedback = {
            "completed_tasks": [
                {"task_id": "nav_to_office", "status": "completed", "duration": 60}
            ],
            "failed_tasks": [
                {"task_id": "nav_to_desk", "status": "failed", "reason": "path_blocked_by_new_chair"}
            ],
            "new_information": {
                "obstacles": [
                    {"type": "chair", "location": {"x": 5.2, "y": 3.3}, "size": {"width": 0.6, "depth": 0.6}}
                ],
                "updated_map": {"obstacle_at_desk_approach": True}
            }
        }

        print("Encountered obstacle - refining plan...")

        # Refine the plan based on new information
        updated_env_state = {
            **original_env_state,
            **execution_feedback["new_information"]
        }

        refined_plan = self.refiner.refine_plan_during_execution(
            original_plan,
            execution_feedback
        )

        return refined_plan, execution_feedback

    def demonstrate_adaptation(self):
        """Demonstrate plan adaptation process"""
        print("Adaptive Planning Demo")
        print("=" * 25)

        # Create original plan
        original_plan, env_state = self.create_original_plan()

        if not original_plan:
            print("Failed to create original plan")
            return

        print("Original plan created successfully")
        print(f"Expected tasks: {len(original_plan.get('tasks', []))}")

        # Simulate execution with obstacle
        refined_plan, feedback = self.simulate_execution_with_obstacle(original_plan, env_state)

        if refined_plan:
            print("\nRefined plan created successfully after obstacle detection")
            print(f"Refined tasks: {len(refined_plan.get('tasks', []))}")
            print(f"Plan validation: {refined_plan.get('validation', {})}")

            # Show differences
            print("\nAdaptation Summary:")
            print(f"- Original plan had {len(original_plan.get('tasks', []))} tasks")
            print(f"- Refined plan has {len(refined_plan.get('tasks', []))} tasks")
            print(f"- Issues identified: {len(refined_plan['validation'].get('issues', []))}")
            print(f"- Suggestions made: {len(refined_plan['validation'].get('suggestions', []))}")
        else:
            print("Failed to create refined plan")

def main():
    demo = AdaptivePlanningDemo()
    demo.demonstrate_adaptation()

if __name__ == "__main__":
    main()
```

## Summary and Next Steps

In this chapter, we've explored the implementation of cognitive planning with Large Language Models (LLMs) for humanoid robotics. Key concepts and techniques covered include:

### Key Concepts Mastered
- **LLM Integration**: Understanding how to effectively integrate LLMs into robotic planning systems for high-level reasoning
- **Reasoning and Decision-Making**: Implementing logical, spatial, and temporal reasoning capabilities for intelligent planning
- **Hierarchical Task Planning**: Breaking down complex tasks into manageable subtasks at different levels of abstraction
- **Plan Refinement and Adaptation**: Creating systems that can modify plans based on execution feedback and changing conditions
- **ROS 2 Integration**: Properly integrating cognitive planning systems with ROS 2 execution frameworks
- **Uncertainty Management**: Handling incomplete information and uncertain environments in planning systems

### Technical Implementation Highlights
- Developed LLM-based planning systems with both cloud and local processing options
- Created hierarchical planning architectures that decompose tasks across multiple abstraction levels
- Implemented reasoning engines for logical, spatial, and temporal reasoning
- Established plan refinement and adaptation mechanisms for dynamic environments
- Created comprehensive integration with ROS 2 execution systems
- Developed practical examples for complex multi-step tasks

### Best Practices Established
- Used appropriate LLM models based on performance and cost requirements
- Implemented fallback systems for robust operation when LLM services are unavailable
- Applied hierarchical decomposition to manage complexity in planning
- Established proper monitoring and adaptation mechanisms for plan execution
- Created modular architecture for easy maintenance and extension

### Performance Considerations
For production LLM-based planning systems, consider:

- **API Costs**: Optimize LLM usage through caching and efficient prompting
- **Latency**: Implement streaming and parallel processing where possible
- **Reliability**: Include fallback mechanisms for when LLM services are unavailable
- **Privacy**: Consider local model deployment for sensitive applications
- **Consistency**: Implement proper prompt engineering for consistent outputs

### Next Steps

With the foundation of cognitive planning with LLMs established, the next chapter will build upon these concepts by exploring the complete Autonomous Humanoid Capstone. We'll cover:

- **Complete VLA Integration**: Bringing together voice, language, and action systems for end-to-end functionality
- **System Architecture**: Designing complete system architectures for autonomous humanoid operation
- **Integration Testing**: Comprehensive testing approaches for complex integrated systems
- **Real-World Deployment**: Practical considerations for deploying complete autonomous systems
- **Advanced AI Techniques**: Implementing more sophisticated AI methods for enhanced autonomy

The knowledge gained in this chapter provides the essential foundation for advanced humanoid robot navigation, combining perception capabilities with intelligent planning to create robots that can understand complex tasks and execute them autonomously.

### Navigation
- **Previous**: [Chapter 1: Voice-to-Action with OpenAI Whisper](./chapter1-voice-to-action-whisper)
- **Next**: [Chapter 3: Capstone - Autonomous Humanoid](./chapter3-autonomous-humanoid-capstone)