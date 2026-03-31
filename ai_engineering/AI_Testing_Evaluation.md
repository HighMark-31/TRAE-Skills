# Skill: AI Testing and Evaluation

## Purpose
To systematically evaluate AI model performance, reliability, and safety using comprehensive testing methodologies and metrics.

## When to Use
- When validating AI models before deployment
- When comparing different models or approaches
- When monitoring model performance in production
- When ensuring AI system reliability and safety

## Procedure

### 1. Model Performance Metrics
Calculate comprehensive performance metrics.

```python
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, classification_report
)

class ModelEvaluator:
    def __init__(self):
        self.metrics = {}
    
    def evaluate_classification(self, y_true, y_pred, y_prob=None):
        """Evaluate classification model performance."""
        self.metrics['accuracy'] = accuracy_score(y_true, y_pred)
        self.metrics['precision'] = precision_score(y_true, y_pred, average='weighted')
        self.metrics['recall'] = recall_score(y_true, y_pred, average='weighted')
        self.metrics['f1_score'] = f1_score(y_true, y_pred, average='weighted')
        
        if y_prob is not None:
            self.metrics['roc_auc'] = roc_auc_score(y_true, y_prob, multi_class='ovr')
        
        # Confusion matrix
        self.metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred)
        
        return self.metrics
    
    def evaluate_regression(self, y_true, y_pred):
        """Evaluate regression model performance."""
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        
        self.metrics['mse'] = mean_squared_error(y_true, y_pred)
        self.metrics['rmse'] = np.sqrt(self.metrics['mse'])
        self.metrics['mae'] = mean_absolute_error(y_true, y_pred)
        self.metrics['r2_score'] = r2_score(y_true, y_pred)
        
        return self.metrics
    
    def generate_report(self):
        """Generate evaluation report."""
        report = "Model Evaluation Report\n"
        report += "=" * 40 + "\n"
        
        for metric, value in self.metrics.items():
            if metric != 'confusion_matrix':
                if isinstance(value, float):
                    report += f"{metric}: {value:.4f}\n"
                else:
                    report += f"{metric}: {value}\n"
        
        return report

# Usage
# evaluator = ModelEvaluator()
# 
# y_true = [0, 1, 2, 1, 0]
# y_pred = [0, 2, 2, 1, 0]
# 
# metrics = evaluator.evaluate_classification(y_true, y_pred)
# print(evaluator.generate_report())
```

### 2. LLM Quality Evaluation
Evaluate language model outputs.

```python
from openai import OpenAI
import json

class LLMEvaluator:
    def __init__(self, model="gpt-4"):
        self.client = OpenAI()
        self.model = model
    
    def evaluate_relevance(self, question, answer, reference_answer=None):
        """Evaluate answer relevance."""
        prompt = f"""
        Question: {question}
        Answer: {answer}
        
        Rate the relevance of this answer to the question on a scale of 1-10.
        Consider: Does it directly address the question? Is it comprehensive?
        
        Provide rating as JSON: {{"relevance_score": <number>, "reasoning": "<explanation>"}}
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except:
            return {"relevance_score": 0, "reasoning": "Failed to parse evaluation"}
    
    def evaluate_accuracy(self, question, answer, ground_truth):
        """Evaluate factual accuracy."""
        prompt = f"""
        Question: {question}
        Generated Answer: {answer}
        Ground Truth: {ground_truth}
        
        Compare the generated answer with the ground truth.
        Rate factual accuracy on a scale of 1-10.
        
        Provide rating as JSON: {{"accuracy_score": <number>, "errors": [<list of factual errors>]}}
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except:
            return {"accuracy_score": 0, "errors": ["Failed to parse evaluation"]}
    
    def evaluate_toxicity(self, text):
        """Check for toxic content."""
        moderation_response = self.client.moderations.create(input=text)
        result = moderation_response.results[0]
        
        return {
            'flagged': result.flagged,
            'categories': result.categories,
            'category_scores': result.category_scores
        }
    
    def batch_evaluate(self, test_cases):
        """Evaluate multiple test cases."""
        results = []
        
        for case in test_cases:
            result = {
                'question': case['question'],
                'answer': case['answer']
            }
            
            # Run evaluations
            result['relevance'] = self.evaluate_relevance(
                case['question'], 
                case['answer']
            )
            
            if 'ground_truth' in case:
                result['accuracy'] = self.evaluate_accuracy(
                    case['question'],
                    case['answer'],
                    case['ground_truth']
                )
            
            result['toxicity'] = self.evaluate_toxicity(case['answer'])
            
            results.append(result)
        
        return results
    
    def calculate_aggregate_metrics(self, evaluation_results):
        """Calculate aggregate metrics across all test cases."""
        metrics = {
            'avg_relevance': np.mean([r['relevance']['relevance_score'] for r in evaluation_results]),
            'flagged_count': sum([1 for r in evaluation_results if r['toxicity']['flagged']]),
            'total_cases': len(evaluation_results)
        }
        
        if 'accuracy' in evaluation_results[0]:
            metrics['avg_accuracy'] = np.mean([r['accuracy']['accuracy_score'] for r in evaluation_results])
        
        return metrics

# Usage
# evaluator = LLMEvaluator()
# 
# test_cases = [
#     {
#         'question': 'What is machine learning?',
#         'answer': 'Machine learning is a subset of AI that enables systems to learn from data.',
#         'ground_truth': 'Machine learning involves training algorithms to make predictions or decisions based on data.'
#     }
# ]
# 
# results = evaluator.batch_evaluate(test_cases)
# aggregate = evaluator.calculate_aggregate_metrics(results)
# print(aggregate)
```

### 3. Robustness Testing
Test model robustness against adversarial inputs.

```python
class RobustnessTester:
    def __init__(self, model):
        self.model = model
    
    def test_typos(self, text, num_variations=5):
        """Test model with typographical variations."""
        variations = []
        
        # Common typos
        common_typos = {
            'the': 'teh',
            'and': 'adn',
            'is': 'si',
            'to': 'ot',
            'of': 'fo'
        }
        
        for _ in range(num_variations):
            variation = text
            for correct, typo in common_typos.items():
                variation = variation.replace(correct, typo)
            variations.append(variation)
        
        return variations
    
    def test_adversarial_examples(self, texts, labels, attack_method='textbugger'):
        """Test against adversarial attacks."""
        # Simplified adversarial example generation
        adversarial_examples = []
        
        for text, label in zip(texts, labels):
            # Add slight perturbations
            words = text.split()
            if len(words) > 0:
                # Duplicate a word
                words.append(words[0])
                adversarial = ' '.join(words)
                adversarial_examples.append((adversarial, label))
        
        return adversarial_examples
    
    def test_out_of_distribution(self, texts):
        """Test with out-of-distribution inputs."""
        ood_cases = [
            # Very short inputs
            "Hi",
            "A",
            "",
            
            # Very long inputs
            "word " * 1000,
            
            # Special characters
            "!@#$%^&*()",
            
            # Mixed languages
            "Hello 你好 Bonjour",
            
            # Malformed inputs
            "...test...",
            "123456789"
        ]
        
        return ood_cases
    
    def evaluate_robustness(self, test_function):
        """Evaluate model robustness."""
        test_cases = {
            'typos': self.test_typos("What is the meaning of life?"),
            'ood': self.test_out_of_distribution([]),
            'adversarial': self.test_adversarial_examples(["Hello world"], [1])
        }
        
        results = {}
        
        for category, cases in test_cases.items():
            results[category] = []
            
            for case in cases:
                try:
                    response = test_function(case)
                    results[category].append({
                        'input': case,
                        'status': 'success',
                        'response': response
                    })
                except Exception as e:
                    results[category].append({
                        'input': case,
                        'status': 'failed',
                        'error': str(e)
                    })
        
        return results

# Usage
# def mock_llm(text):
#     return f"Response to: {text[:50]}"
# 
# tester = RobustnessTester(model=None)
# robustness_results = tester.evaluate_robustness(mock_llm)
```

### 4. A/B Testing Framework
Implement A/B testing for model comparison.

```python
from scipy import stats

class ABTestFramework:
    def __init__(self):
        self.results = {'A': [], 'B': []}
    
    def add_result(self, group, metric_value):
        """Add a result for a group."""
        if group in ['A', 'B']:
            self.results[group].append(metric_value)
    
    def calculate_significance(self, metric='accuracy'):
        """Calculate statistical significance."""
        group_a = self.results['A']
        group_b = self.results['B']
        
        # T-test
        t_statistic, p_value = stats.ttest_ind(group_a, group_b)
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(group_a)**2 + np.std(group_b)**2) / 2)
        cohens_d = (np.mean(group_a) - np.mean(group_b)) / pooled_std
        
        return {
            'group_a_mean': np.mean(group_a),
            'group_b_mean': np.mean(group_b),
            't_statistic': t_statistic,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'cohens_d': cohens_d
        }
    
    def generate_report(self):
        """Generate A/B test report."""
        stats = self.calculate_significance()
        
        report = f"""
A/B Test Results Report
{'=' * 50}

Group A: n={len(self.results['A'])}, mean={stats['group_a_mean']:.4f}
Group B: n={len(self.results['B'])}, mean={stats['group_b_mean']:.4f}

Statistical Analysis:
- t-statistic: {stats['t_statistic']:.4f}
- p-value: {stats['p_value']:.4f}
- Significant: {'Yes' if stats['significant'] else 'No'}
- Effect size (Cohen's d): {stats['cohens_d']:.4f}

Conclusion:
"""
        if stats['significant']:
            if stats['group_a_mean'] > stats['group_b_mean']:
                report += "Group A performs significantly better than Group B."
            else:
                report += "Group B performs significantly better than Group A."
        else:
            report += "No significant difference found between groups."
        
        return report

# Usage
# ab_test = ABTestFramework()
# 
# # Add results (in practice, these come from user interactions)
# for _ in range(100):
#     ab_test.add_result('A', np.random.normal(0.7, 0.1))
#     ab_test.add_result('B', np.random.normal(0.75, 0.1))
# 
# print(ab_test.generate_report())
```

## Constraints
- **Ground Truth**: High-quality ground truth data is essential for accurate evaluation
- **Bias in Evaluation**: Evaluation metrics themselves may contain biases
- **Context Dependency**: Performance may vary significantly across different contexts
- **Cost**: Comprehensive evaluation can be expensive, especially for LLMs
- **Subjectivity**: Some metrics (like quality) are inherently subjective
- **Dynamic Performance**: Model performance may degrade over time

## Expected Output
Comprehensive evaluation of AI systems with detailed metrics, robustness testing results, and statistical analysis to ensure reliable and safe deployment.
