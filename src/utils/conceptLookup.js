import conceptsData from '../data/concepts.json';

// Build lookup maps for instant O(1) matching
const subtopicToConceptMap = new Map();

for (const concept of conceptsData) {
  if (concept.raw_subtopic) subtopicToConceptMap.set(concept.raw_subtopic.trim(), concept);
  if (concept.raw_sub) subtopicToConceptMap.set(concept.raw_sub.trim(), concept);
  if (concept.title) subtopicToConceptMap.set(concept.title.trim(), concept);
  if (concept.id) subtopicToConceptMap.set(concept.id.trim(), concept);
}

/**
 * Finds the corresponding concept for a given subtopic string and optional topic ID.
 */
export function findConceptForSubtopic(subtopicName, topicId = null) {
  if (!subtopicName) return null;
  const trimmed = subtopicName.trim();

  // 1. Direct exact match
  if (subtopicToConceptMap.has(trimmed)) {
    return subtopicToConceptMap.get(trimmed);
  }

  // 2. Scoped topic search
  if (topicId) {
    const topicMatch = conceptsData.find((c) => {
      if (c.topic_id !== topicId) return false;
      const tLower = (c.title || '').toLowerCase();
      const rLower = (c.raw_subtopic || '').toLowerCase();
      const sLower = trimmed.toLowerCase();
      return tLower.includes(sLower) || sLower.includes(tLower) || rLower.includes(sLower);
    });
    if (topicMatch) return topicMatch;
  }

  // 3. Global fuzzy match
  const sLower = trimmed.toLowerCase();
  const globalMatch = conceptsData.find((c) => {
    const tLower = (c.title || '').toLowerCase();
    const rLower = (c.raw_subtopic || '').toLowerCase();
    return tLower.includes(sLower) || sLower.includes(tLower) || rLower.includes(sLower);
  });

  return globalMatch || null;
}

/**
 * Returns the target URL to redirect to the concept's full explanation page.
 */
export function getConceptRedirectUrl(subtopicName, topicId = null) {
  const concept = findConceptForSubtopic(subtopicName, topicId);
  if (concept && concept.id) {
    return `/concepts?id=${encodeURIComponent(concept.id)}`;
  }
  return `/concepts?search=${encodeURIComponent(subtopicName)}`;
}
