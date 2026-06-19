'use client'

import { useRef } from 'react'
import Image from 'next/image'
import { useMouseParallax } from '@/lib/useMouseParallax'
import styles from '@/styles/ui/ParallaxPhotoLayers.module.css'

/**
 * Full-bleed background (+ optional mid) photo layers with mouse parallax.
 * background: { src, opacity?, blur?, position?, scale?, priority? }
 * midground?: same shape — sits between bg and content
 */
export default function ParallaxPhotoLayers({ background, midground, className = '', variant = 'default' }) {
  const wrapRef = useRef(null)
  const bgRef   = useRef(null)
  const midRef  = useRef(null)

  const layers = [{ ref: bgRef, x: 28, y: 18 }]
  if (midground) layers.push({ ref: midRef, x: -16, y: -10 })
  useMouseParallax(wrapRef, layers)

  if (!background?.src) return null

  const bgOpacity = background.opacity ?? 0.28
  const bgBlur    = background.blur ?? 6
  const bgScale   = background.scale ?? 1.08

  return (
    <div ref={wrapRef} className={`${styles.wrap} ${className}`} aria-hidden>
      <div
        ref={bgRef}
        className={styles.layer}
        style={{
          opacity: bgOpacity,
          filter: `blur(${bgBlur}px) saturate(0.9)`,
          transform: `scale(${bgScale})`,
        }}
      >
        <Image
          src={background.src}
          alt=""
          fill
          quality={85}
          sizes="100vw"
          className={styles.img}
          style={{ objectPosition: background.position ?? 'center 30%' }}
          priority={background.priority ?? false}
        />
      </div>

      {midground?.src && (
        <div
          ref={midRef}
          className={styles.midLayer}
          style={{
            opacity: midground.opacity ?? 0.12,
            filter: midground.blur ? `blur(${midground.blur}px)` : undefined,
          }}
        >
          <Image
            src={midground.src}
            alt=""
            fill
            quality={80}
            sizes="60vw"
            className={styles.img}
            style={{ objectPosition: midground.position ?? 'center bottom' }}
          />
        </div>
      )}

      <div className={`${styles.scrim} ${variant === 'side' ? styles.scrimSide : ''}`} />
    </div>
  )
}
