import { useEffect } from 'react';

type KeyHandler = (event: KeyboardEvent) => void;

export function useKeyboardShortcut(
  targetKey: string,
  handler: KeyHandler,
  options: { ctrlOrCmd?: boolean } = {}
) {
  useEffect(() => {
    const listener = (event: KeyboardEvent) => {
      const isCtrlOrCmd = options.ctrlOrCmd ? event.ctrlKey || event.metaKey : true;
      if (isCtrlOrCmd && event.key.toLowerCase() === targetKey.toLowerCase()) {
        event.preventDefault();
        handler(event);
      }
    };

    window.addEventListener('keydown', listener);
    return () => window.removeEventListener('keydown', listener);
  }, [targetKey, handler, options]);
}
