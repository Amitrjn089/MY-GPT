import { useEffect, useRef } from "react";

export default function AudioPlayer({ audioQueue }) {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioQueue.length === 0) return;

    const blob = audioQueue[0];
    const url = URL.createObjectURL(blob);

    audioRef.current.src = url;
    audioRef.current.play();

    audioRef.current.onended = () => {
      URL.revokeObjectURL(url);
    };
  }, [audioQueue]);

  return <audio ref={audioRef} />;
}
