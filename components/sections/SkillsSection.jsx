'use client'

import { useEffect, useRef } from 'react'
import { gsap } from '@/lib/gsap'
import ParallaxPhotoLayers from '@/components/ui/ParallaxPhotoLayers'
import profile from '@/data/profile.json'
import styles from '@/styles/sections/SkillsSection.module.css'

const SKILL_GROUPS = profile.skillGroups ?? []

export default function SkillsSection() {
  const sectionRef = useRef(null)
  const headerRef  = useRef(null)
  const gridRef    = useRef(null)

  useEffect(() => {
    const section = sectionRef.current
    if (!section) return
    const scroller = document.querySelector('main')
    if (!scroller) return

    let active = false

    function reset() {
      gsap.set(headerRef.current, { opacity: 0, y: 24 })
      gsap.set(gridRef.current?.children ?? [], { opacity: 0, y: 20 })
    }

    function play() {
      reset()
      gsap.to(headerRef.current, { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' })
      gsap.to(gridRef.current?.children ?? [], {
        opacity: 1, y: 0, duration: 0.55, ease: 'power2.out', stagger: 0.08, delay: 0.15,
      })
    }

    reset()

    function onScroll() {
      const inRange = Math.abs(scroller.scrollTop - section.offsetTop) < window.innerHeight * 0.45
      if (inRange && !active) { active = true; play() }
      if (!inRange && active) { active = false; reset() }
    }

    scroller.addEventListener('scroll', onScroll, { passive: true })
    return () => scroller.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <section ref={sectionRef} className={styles.section}>
      <ParallaxPhotoLayers
        background={{ src: '/assets/hero-foreground.png', opacity: 0.08, blur: 8, position: 'center 30%' }}
      />

      <div ref={headerRef} className={styles.header}>
        <span className={styles.label}>Technical Skills</span>
        <h2 className={styles.title}>Skills &amp; Stack</h2>
        <p className={styles.subtitle}>
          {SKILL_GROUPS.length} technical skill areas — {profile.roles.detailed}
        </p>
      </div>

      <div ref={gridRef} className={styles.grid}>
        {SKILL_GROUPS.map(group => (
          <div key={group.title} className={styles.card}>
            <h3 className={styles.cardTitle}>{group.title}</h3>
            <div className={styles.tags}>
              {group.items.map(skill => (
                <span key={skill} className={styles.tag}>{skill}</span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className={styles.marqueeWrap}>
        <div className={styles.marqueeTrack}>
          {[...profile.skills, ...profile.skills].map((skill, i) => (
            <span key={`${skill}-${i}`} className={styles.marqueeItem}>
              {skill}<span className={styles.dot}>·</span>
            </span>
          ))}
        </div>
      </div>
    </section>
  )
}
