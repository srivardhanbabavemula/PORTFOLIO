'use client'

import { useEffect } from 'react'
import { gsap } from '@/lib/gsap'

/** Subtle mouse-driven parallax for foreground / background layers */
export function useMouseParallax(containerRef, layers, enabled = true) {
  useEffect(() => {
    if (!enabled) return
    const el = containerRef.current
    if (!el || !layers?.length) return

    function onMove(e) {
      const r = el.getBoundingClientRect()
      const mx = (e.clientX - r.left) / r.width - 0.5
      const my = (e.clientY - r.top) / r.height - 0.5
      layers.forEach(({ ref, x = 20, y = 12 }) => {
        if (!ref.current) return
        gsap.to(ref.current, {
          x: mx * x,
          y: my * y,
          duration: 0.85,
          ease: 'power2.out',
          overwrite: 'auto',
        })
      })
    }

    el.addEventListener('mousemove', onMove)
    return () => el.removeEventListener('mousemove', onMove)
  }, [containerRef, layers, enabled])
}

/** Gentle floating animation (y-axis bob) */
export function useFloatAnimation(ref, { y = 14, duration = 3.8 } = {}) {
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const tween = gsap.to(el, {
      y,
      duration,
      ease: 'sine.inOut',
      yoyo: true,
      repeat: -1,
    })
    return () => tween.kill()
  }, [ref, y, duration])
}

/** 3D tilt on hover for card / photo frames */
export function useTilt3D(ref, maxDeg = 8) {
  useEffect(() => {
    const el = ref.current
    if (!el) return

    function onMove(e) {
      const r = el.getBoundingClientRect()
      const px = (e.clientX - r.left) / r.width - 0.5
      const py = (e.clientY - r.top) / r.height - 0.5
      gsap.to(el, {
        rotateY: px * maxDeg,
        rotateX: -py * maxDeg,
        transformPerspective: 900,
        duration: 0.35,
        ease: 'power2.out',
      })
    }

    function onLeave() {
      gsap.to(el, {
        rotateY: 0,
        rotateX: 0,
        duration: 0.6,
        ease: 'power3.out',
      })
    }

    el.addEventListener('mousemove', onMove)
    el.addEventListener('mouseleave', onLeave)
    return () => {
      el.removeEventListener('mousemove', onMove)
      el.removeEventListener('mouseleave', onLeave)
    }
  }, [ref, maxDeg])
}
