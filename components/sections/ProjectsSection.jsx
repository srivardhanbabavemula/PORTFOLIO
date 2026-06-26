'use client'

import { useEffect, useRef } from 'react'
import Image from 'next/image'
import { gsap, ScrollTrigger } from '@/lib/gsap'
import profile from '@/data/profile.json'
import styles from '@/styles/sections/ProjectsSection.module.css'

const PROJECTS = profile.projects

export default function ProjectsSection() {
  const sectionRef  = useRef(null)
  const slideRefs   = useRef([])
  const counterRef  = useRef(null)
  const progressRef = useRef(null)
  const activeRef   = useRef(0)

  useEffect(() => {
    const section = sectionRef.current
    if (!section) return

    const scroller = document.querySelector('main')
    if (!scroller) return
    const n = PROJECTS.length
    slideRefs.current = slideRefs.current.slice(0, n)

    slideRefs.current.forEach((el, i) => {
      if (el) gsap.set(el, { autoAlpha: i === 0 ? 1 : 0, pointerEvents: i === 0 ? 'auto' : 'none' })
    })

    const st = ScrollTrigger.create({
      trigger: section,
      scroller,
      start: 'top top',
      end: () => `+=${(n - 1) * window.innerHeight}`,
      onUpdate: (self) => {
        const active = Math.round(self.progress * (n - 1))
        if (active === activeRef.current) return
        activeRef.current = active

        slideRefs.current.forEach((el, i) => {
          if (!el) return
          const on = i === active
          gsap.set(el, { autoAlpha: on ? 1 : 0, pointerEvents: on ? 'auto' : 'none' })
        })

        if (progressRef.current) {
          gsap.set(progressRef.current, {
            scaleX: self.progress,
            transformOrigin: 'left center',
            overwrite: true,
          })
        }
        if (counterRef.current) {
          counterRef.current.textContent = String(active + 1).padStart(2, '0')
        }
      },
    })

    return () => st.kill()
  }, [])

  return (
    <div className={styles.wrapper} style={{ height: `${PROJECTS.length * 100}vh` }} data-snap-anchor="projects">
      <section ref={sectionRef} className={styles.section}>

        <div className={styles.topBar}>
          <span className={styles.sectionLabel}>Featured Work</span>
          <div className={styles.counter}>
            <span ref={counterRef} className={styles.cCur}>01</span>
            <span className={styles.cSep}> / </span>
            <span className={styles.cTot}>0{PROJECTS.length}</span>
          </div>
        </div>

        <div className={styles.track}>
          {PROJECTS.map((proj, i) => (
            <div
              key={proj.id}
              ref={el => { slideRefs.current[i] = el }}
              className={styles.slide}
            >
              {proj.bgImage && (
                <div className={styles.slideBg} aria-hidden>
                  <div className={styles.slideBgInner}>
                    <Image
                      src={proj.bgImage}
                      alt=""
                      fill
                      quality={90}
                      className={styles.slideBgImg}
                      sizes="100vw"
                      priority={i === 0}
                    />
                  </div>
                </div>
              )}
              <span className={styles.slideNum} aria-hidden>0{i + 1}</span>

              <div className={styles.slideContent}>
                <div className={styles.meta}>
                  <span className={styles.typeTag}>{proj.type}</span>
                </div>
                <h2 className={styles.title}>{proj.title}</h2>
                <p className={styles.subtitle}>{proj.subtitle}</p>
                <p className={styles.desc}>{proj.desc}</p>
                {proj.context && <p className={styles.context}>{proj.context}</p>}
                <div className={styles.stack}>
                  {proj.tech.map(t => (
                    <span key={t} className={styles.tag}>{t}</span>
                  ))}
                </div>
                <a
                  href={proj.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.liveBtn}
                >
                  <span>View on GitHub</span>
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden>
                    <path d="M2 10L10 2M10 2H4M10 2V8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </a>
              </div>

              <div className={styles.visualPanel}>
                <Image
                  src={proj.image}
                  alt={`${proj.title} cover`}
                  fill
                  quality={95}
                  className={styles.visualImg}
                  sizes="(min-width: 768px) 45vw, 90vw"
                  priority={i === 0}
                />
              </div>
            </div>
          ))}
        </div>

        <div className={styles.bottomUI}>
          <div className={styles.progressTrack}>
            <div ref={progressRef} className={styles.progressBar} />
          </div>
        </div>

      </section>
    </div>
  )
}
