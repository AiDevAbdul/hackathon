import React, { useState } from 'react';

const PreferencesForm = ({ onSubmit, initialData = {}, onCancel }) => {
  const [formData, setFormData] = useState({
    content_level_preference: initialData.content_level_preference || '',
    example_preference: initialData.example_preference || '',
    detail_preference: initialData.detail_preference || '',
    learning_path: initialData.learning_path || []
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="personalization-form">
      <h3>Personalization Preferences</h3>

      <div className="form-group">
        <label htmlFor="content_level_preference">Content Level Preference:</label>
        <select
          id="content_level_preference"
          name="content_level_preference"
          value={formData.content_level_preference}
          onChange={handleInputChange}
        >
          <option value="">Select your preferred level</option>
          <option value="beginner">Beginner - Simple explanations and basic concepts</option>
          <option value="intermediate">Intermediate - Moderate complexity with examples</option>
          <option value="advanced">Advanced - In-depth technical details and theory</option>
        </select>
        <p className="form-help">Choose the level of complexity you prefer for content.</p>
      </div>

      <div className="form-group">
        <label htmlFor="example_preference">Example Preference:</label>
        <select
          id="example_preference"
          name="example_preference"
          value={formData.example_preference}
          onChange={handleInputChange}
        >
          <option value="">Select your preferred example type</option>
          <option value="theoretical">Theoretical - Conceptual and academic examples</option>
          <option value="practical">Practical - Real-world applications and use cases</option>
        </select>
        <p className="form-help">Choose the type of examples that help you learn best.</p>
      </div>

      <div className="form-group">
        <label htmlFor="detail_preference">Detail Preference:</label>
        <select
          id="detail_preference"
          name="detail_preference"
          value={formData.detail_preference}
          onChange={handleInputChange}
        >
          <option value="">Select your preferred detail level</option>
          <option value="concise">Concise - Key points and summaries</option>
          <option value="detailed">Detailed - Comprehensive explanations</option>
        </select>
        <p className="form-help">Choose how detailed you want the explanations to be.</p>
      </div>

      <div className="form-actions">
        <button type="submit">Save Preferences</button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="cancel-button">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default PreferencesForm;