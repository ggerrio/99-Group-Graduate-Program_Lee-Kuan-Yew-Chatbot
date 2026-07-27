import { useEffect, useRef, RefObject } from 'react';

export function useAutoScroll<T extends HTMLElement>(dependencies: unknown[]): RefObject<T | null> {
  const containerRef = useRef<T | null>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo({
        top: containerRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencies);

  return containerRef;
}
