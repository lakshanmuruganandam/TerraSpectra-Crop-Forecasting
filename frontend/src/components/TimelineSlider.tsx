import React, { useEffect } from 'react'
import { Play, Pause, Calendar, RotateCcw } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'

const WEEKS = [
  { label: 'Week 1 (Baseline)', date: '2026-07-01' },
  { label: 'Week 2 (Incipient)', date: '2026-07-08' },
  { label: 'Week 3 (Outbreak)', date: '2026-07-15' },
  { label: 'Week 4 (Peak Spread)', date: '2026-07-22' },
]

export const TimelineSlider: React.FC = () => {
  const { activeWeekIndex, setActiveWeekIndex, isPlayingTimeline, setIsPlayingTimeline } =
    useAppStore()

  // Automated playback timer
  useEffect(() => {
    let timer: any = null
    if (isPlayingTimeline) {
      timer = setInterval(() => {
        setActiveWeekIndex((activeWeekIndex + 1) % WEEKS.length)
      }, 1800)
    }
    return () => {
      if (timer) clearInterval(timer)
    }
  }, [isPlayingTimeline, activeWeekIndex, setActiveWeekIndex])

  return (
    <div className="absolute bottom-6 left-1/2 z-40 -translate-x-1/2 w-full max-w-lg rounded-2xl border border-white/10 bg-neutral-950/85 p-3.5 shadow-2xl backdrop-blur-xl transition-all sm:w-auto">
      <div className="flex items-center gap-4">
        {/* Play/Pause Button */}
        <button
          onClick={() => setIsPlayingTimeline(!isPlayingTimeline)}
          className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 transition-all hover:bg-emerald-500/30 hover:scale-105 active:scale-95"
        >
          {isPlayingTimeline ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5 ml-0.5" />}
        </button>

        {/* Timeline Slider Track */}
        <div className="flex flex-1 flex-col gap-1.5 min-w-[240px]">
          <div className="flex items-center justify-between text-xs">
            <span className="flex items-center gap-1.5 font-medium text-neutral-200">
              <Calendar className="h-3.5 w-3.5 text-emerald-400" />
              {WEEKS[activeWeekIndex].label}
            </span>
            <span className="font-mono text-[11px] text-neutral-400">
              {WEEKS[activeWeekIndex].date}
            </span>
          </div>

          <input
            type="range"
            min="0"
            max={WEEKS.length - 1}
            step="1"
            value={activeWeekIndex}
            onChange={(e) => setActiveWeekIndex(parseInt(e.target.value))}
            className="h-2 cursor-pointer accent-emerald-500 bg-neutral-800 rounded-lg"
          />
        </div>

        {/* Reset Button */}
        <button
          onClick={() => {
            setIsPlayingTimeline(false)
            setActiveWeekIndex(0)
          }}
          title="Reset to Week 1"
          className="flex h-9 w-9 items-center justify-center rounded-xl border border-neutral-800 bg-neutral-900/60 text-neutral-400 transition-colors hover:text-white hover:border-neutral-700"
        >
          <RotateCcw className="h-4 w-4" />
        </button>
      </div>
    </div>
  )
}
