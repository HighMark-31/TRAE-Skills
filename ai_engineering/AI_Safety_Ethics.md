# Skill: AI Safety and Ethics

## Purpose
To implement AI systems that are safe, fair, transparent, and aligned with human values while minimizing potential harms and biases.

## When to Use
- When deploying AI systems that affect people's lives
- When working with sensitive data or protected characteristics
- When implementing automated decision-making systems
- When ensuring regulatory compliance (GDPR, AI Act, etc.)

## Procedure

### 1. Bias Detection and Mitigation
Identify and reduce biases in AI systems.

```python
import pandas as pd
from sklearn.metrics import confusion_matrix
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing

def detect_bias(df, protected_attribute, label, privileged_groups, unprivileged_groups):
    """Detect bias in dataset."""
    # Convert to AIF360 dataset
    dataset = BinaryLabelDataset(
        df=df,
        label_names=[label],
        protected_attribute_names=[protected_attribute],
        favorable_label=1,
        unfavorable_label=0
    )
    
    # Calculate fairness metrics
    metric = BinaryLabelDatasetMetric(
        dataset,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
    
    return {
        'disparate_impact': metric.disparate_impact(),
        'statistical_parity_difference': metric.statistical_parity_difference()
    }

def mitigate_bias(df, protected_attribute, label, privileged_groups, unprivileged_groups):
    """Apply bias mitigation techniques."""
    # Original dataset
    dataset = BinaryLabelDataset(
        df=df,
        label_names=[label],
        protected_attribute_names=[protected_attribute],
        favorable_label=1,
        unfavorable_label=0
    )
    
    # Apply reweighing
    reweigher = Reweighing(
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
    
    dataset_transformed = reweigher.fit_transform(dataset)
    
    return dataset_transformed.convert_to_dataframe()[0]

# Example usage
# df = pd.read_csv('loan_applications.csv')
# protected_attribute = 'gender'
# label = 'loan_approved'
# 
# bias_metrics = detect_bias(df, protected_attribute, label, 
#                             privileged_groups=[{'gender': 1}],
#                             unprivileged_groups=[{'gender': 0}])
# 
# print(f"Disparate Impact: {bias_metrics['disparate_impact']}")
# 
# # Mitigate bias
# fair_df = mitigate_bias(df, protected_attribute, label,
#                         privileged_groups=[{'gender': 1}],
#                         unprivileged_groups=[{'gender': 0}])
```

### 2. Content Moderation and Safety
Implement safety filters for AI content.

```python
import openai

class SafeContentGenerator:
    def __init__(self):
        self.client = openai.OpenAI()
        self.forbidden_categories = [
            "hate speech",
            "violence",
            "self-harm",
            "sexual content",
            "illegal activities"
        ]
    
    def check_safety(self, content):
        """Check if content is safe."""
        moderation_response = self.client.moderations.create(input=content)
        result = moderation_response.results[0]
        
        return {
            'flagged': result.flagged,
            'categories': result.categories,
            'category_scores': result.category_scores
        }
    
    def generate_safe_content(self, prompt, max_retries=3):
        """Generate content with safety checks."""
        for attempt in range(max_retries):
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            safety_check = self.check_safety(content)
            
            if not safety_check['flagged']:
                return content
            
            print(f"Attempt {attempt + 1}: Content flagged as unsafe")
            prompt = f"Generate content that is completely safe and appropriate: {prompt}"
        
        raise Exception("Failed to generate safe content after multiple attempts")

# Usage
generator = SafeContentGenerator()
safe_content = generator.generate_safe_content("Write a story about teamwork")
```

### 3. Transparency and Explainability
Implement explainability for AI decisions.

```python
import shap
from sklearn.ensemble import RandomForestClassifier

class ExplainableAI:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
    
    def fit_explainer(self, X_train):
        """Fit SHAP explainer."""
        self.explainer = shap.Explainer(self.model, X_train)
    
    def explain_prediction(self, instance):
        """Explain individual prediction."""
        shap_values = self.explainer(instance)
        
        # Get feature importance
        feature_importance = list(zip(
            self.feature_names,
            shap_values.values[0]
        ))
        
        # Sort by absolute importance
        feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
        
        return feature_importance[:10]  # Top 10 features
    
    def generate_explanation_text(self, instance, prediction, feature_importance):
        """Generate human-readable explanation."""
        explanation = f"Prediction: {prediction}\n\n"
        explanation += "Key factors influencing this decision:\n"
        
        for feature, importance in feature_importance:
            direction = "increases" if importance > 0 else "decreases"
            explanation += f"- {feature}: {direction} likelihood (impact: {abs(importance):.3f})\n"
        
        return explanation

# Example usage
# model = RandomForestClassifier()
# model.fit(X_train, y_train)
# 
# explainable_ai = ExplainableAI(model, feature_names)
# explainable_ai.fit_explainer(X_train)
# 
# instance = X_test[0]
# prediction = model.predict([instance])[0]
# feature_importance = explainable_ai.explain_prediction(instance)
# 
# explanation = explainable_ai.generate_explanation_text(
#     instance, prediction, feature_importance
# )
# print(explanation)
```

### 4. Privacy-Preserving AI
Implement privacy protection in AI systems.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

class PrivacyPreservingML:
    def __init__(self, epsilon=1.0):
        self.epsilon = epsilon
        self.scaler = StandardScaler()
    
    def add_laplace_noise(self, data, sensitivity):
        """Add Laplace noise for differential privacy."""
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale, data.shape)
        return data + noise
    
    def private_aggregation(self, data):
        """Perform differentially private aggregation."""
        sensitivity = 1.0  # Depends on the query
        noisy_mean = self.add_laplace_noise(data, sensitivity)
        return np.mean(noisy_mean)
    
    def anonymize_data(self, df, sensitive_columns):
        """Anonymize sensitive data."""
        df_anon = df.copy()
        
        for column in sensitive_columns:
            # Generalize or remove sensitive information
            if df[column].dtype == 'object':
                # Categorical: use frequency encoding
                freq = df[column].value_counts(normalize=True)
                df_anon[column] = df[column].map(freq)
            else:
                # Numerical: add noise
                df_anon[column] = self.add_laplace_noise(
                    df[column].values, 
                    sensitivity=df[column].max()
                )
        
        return df_anon
    
    def federated_learning_step(self, local_models, global_model):
        """Simulate federated learning update."""
        # Aggregate local model updates
        averaged_weights = []
        
        for weights_list in zip(*[model.get_weights() for model in local_models]):
            averaged_weights.append(np.mean(weights_list, axis=0))
        
        # Update global model
        global_model.set_weights(averaged_weights)
        return global_model

# Usage
# privacy_ml = PrivacyPreservingML(epsilon=0.5)
# 
# # Anonymize data
# sensitive_data = df[['age', 'income', 'zip_code']]
# df_anon = privacy_ml.anonymize_data(df, ['age', 'income'])
```

### 5. Ethical Review Framework
Implement ethical review for AI systems.

```python
class EthicalReviewer:
    def __init__(self):
        self.checklist = {
            'fairness': [
                'Have we tested for bias across demographic groups?',
                'Are the training datasets representative?',
                'Have we implemented fairness metrics?'
            ],
            'transparency': [
                'Can we explain individual decisions?',
                'Are users informed about AI involvement?',
                'Is the system\'s limitations documented?'
            ],
            'accountability': [
                'Is there a human in the loop?',
                'Can decisions be appealed?',
                'Are logs maintained for audit?'
            ],
            'safety': [
                'Have we implemented safety guards?',
                'Is there content moderation?',
                'Are there fail-safe mechanisms?'
            ],
            'privacy': [
                'Is user data protected?',
                'Have we obtained proper consent?',
                'Is data minimization applied?'
            ]
        }
    
    def review_system(self, responses):
        """Review AI system against ethical checklist."""
        results = {}
        
        for category, questions in self.checklist.items():
            category_score = 0
            category_responses = []
            
            for i, question in enumerate(questions):
                response = responses.get(f"{category}_{i}", "not_answered")
                
                if response.lower() in ['yes', 'implemented', 'yes_implemented']:
                    category_score += 1
                    status = "✓"
                elif response.lower() == 'partially':
                    category_score += 0.5
                    status = "~"
                else:
                    status = "✗"
                
                category_responses.append({
                    'question': question,
                    'response': response,
                    'status': status
                })
            
            results[category] = {
                'score': category_score / len(questions),
                'responses': category_responses
            }
        
        return results
    
    def generate_report(self, review_results):
        """Generate ethical review report."""
        report = "AI System Ethical Review Report\n"
        report += "=" * 50 + "\n\n"
        
        for category, data in review_results.items():
            score_percent = data['score'] * 100
            report += f"{category.upper()}: {score_percent:.0f}%\n"
            
            for response in data['responses']:
                report += f"  {response['status']} {response['question']}\n"
                report += f"      Response: {response['response']}\n"
            
            report += "\n"
        
        overall_score = np.mean([data['score'] for data in review_results.values()])
        report += f"\nOVERALL ETHICAL SCORE: {overall_score * 100:.0f}%\n"
        
        if overall_score >= 0.8:
            report += "Status: PASS - System meets ethical standards\n"
        elif overall_score >= 0.6:
            report += "Status: CONDITIONAL - Address identified concerns\n"
        else:
            report += "Status: FAIL - Significant ethical concerns\n"
        
        return report

# Usage
# reviewer = EthicalReviewer()
# 
# responses = {
#     'fairness_0': 'yes',
#     'fairness_1': 'partially',
#     'transparency_0': 'yes',
#     # ... more responses
# }
# 
# results = reviewer.review_system(responses)
# report = reviewer.generate_report(results)
# print(report)
```

## Constraints
- **Legal Compliance**: Ensure compliance with relevant laws and regulations
- **Context Dependency**: Ethical considerations vary by application and culture
- **Trade-offs**: Balance between competing ethical principles may be necessary
- **Continuous Monitoring**: Ethical behavior requires ongoing monitoring and updates
- **Stakeholder Involvement**: Include diverse stakeholders in ethical assessments
- **Transparency Limits**: Some models are inherently difficult to explain

## Expected Output
AI systems that are safe, fair, transparent, and aligned with ethical principles, with proper documentation and monitoring for responsible deployment.
