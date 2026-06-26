'use client'

import { useEffect, useRef, useState } from 'react'
import { FiArrowUpRight } from 'react-icons/fi'
import { gsap } from '@/lib/gsap'
import profile from '@/data/profile.json'
import CertPreviewModal from '@/components/ui/CertPreviewModal'
import styles from '@/styles/sections/CertificationsSection.module.css'

const CERTS = profile.publications.filter(c => c.title !== 'Certificate of Skills Portfolio')

export default function CertificationsSection() {
  const sectionRef = useRef(null)
  const headerRef  = useRef(null)
  const listRef    = useRef(null)
  const [activeCert, setActiveCert] = useState(null)

  useEffect(() => {
    const section = sectionRef.current
    if (!section) return
    const scroller = document.querySelector('main')
    if (!scroller) return

    let active = false

    function reset() {
      gsap.set(headerRef.current, { opacity: 0, y: 20 })
      gsap.set(listRef.current?.children ?? [], { opacity: 0, x: -16 })
    }

    function play() {
      reset()
      gsap.to(headerRef.current, { opacity: 1, y: 0, duration: 0.65, ease: 'power3.out' })
      gsap.to(listRef.current?.children ?? [], {
        opacity: 1, x: 0, duration: 0.5, ease: 'power2.out', stagger: 0.04, delay: 0.12,
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

  function openCert(cert) {
    if (cert.certImage) setActiveCert(cert)
    else if (cert.link?.startsWith('http')) window.open(cert.link, '_blank', 'noopener,noreferrer')
  }

  return (
    <>
      <section ref={sectionRef} className={styles.section} data-snap-anchor="certifications">
        <div ref={headerRef} className={styles.header}>
          <span className={styles.label}>Credentials</span>
          <h2 className={styles.title}>Certifications</h2>
          <p className={styles.subtitle}>
            {CERTS.length} professional certifications — click any entry to preview the certificate image.
          </p>
        </div>

        <div ref={listRef} className={styles.list}>
          {CERTS.map((cert, i) => (
            <button
              key={cert.id}
              type="button"
              className={styles.card}
              onClick={() => openCert(cert)}
            >
              <span className={styles.num}>{String(i + 1).padStart(2, '0')}</span>
              <div className={styles.body}>
                <h3 className={styles.cardTitle}>{cert.title}</h3>
                <p className={styles.platform}>{cert.platform} · {cert.year}</p>
                <p className={styles.desc}>{cert.desc}</p>
              </div>
              <span className={styles.arrow}>
                {cert.certImage ? 'Preview' : <FiArrowUpRight />}
              </span>
            </button>
          ))}
        </div>
      </section>

      <CertPreviewModal cert={activeCert} onClose={() => setActiveCert(null)} />
    </>
  )
}
