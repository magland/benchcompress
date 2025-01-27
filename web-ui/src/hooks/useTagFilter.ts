import { useState, useMemo } from "react";

interface TaggableItem {
  tags: string[];
}

export function useTagFilter<T extends TaggableItem>(items: T[]) {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const availableTags = useMemo(() => {
    const tagSet = new Set<string>();
    items.forEach((item) => {
      item.tags.forEach((tag) => tagSet.add(tag));
    });
    return Array.from(tagSet).sort();
  }, [items]);

  const filteredItems = useMemo(() => {
    if (selectedTags.length === 0) return items;
    return items.filter((item) =>
      selectedTags.every((tag) => item.tags.includes(tag)),
    );
  }, [items, selectedTags]);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag],
    );
  };

  return {
    selectedTags,
    availableTags,
    filteredItems,
    toggleTag,
  };
}
