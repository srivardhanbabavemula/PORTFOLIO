'use client'

import { useEffect } from 'react'
import Image from 'next/image'
import { FiX, FiExternalLink } from 'react-icons/fi'
import styles from '@/styles/ui/CertPreviewModal.module.css'

export default function CertPreviewModal({ cert, onClose }) {
  useEffect(() => {
    if (!cert) return
    function onKey(e) {
      if (e.key === 'Escape') onClose()
    }
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', onKey)
    return () => {
      document.body.style.overflow = ''
      window.removeEventListener('keydown', onKey)
    }
  }, [cert, onClose])

  if (!cert) return null

  return (
    <div className={styles.backdrop} onClick={onClose} role="presentation">
      <div
        className={styles.dialog}
        onClick={e => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="cert-modal-title"
      >
        <header className={styles.header}>
          <div>
            <p className={styles.eyebrow}>{cert.platform} · {cert.year}</p>
            <h3 id="cert-modal-title" className={styles.title}>{cert.title}</h3>
          </div>
          <button type="button" className={styles.closeBtn} onClick={onClose} aria-label="Close">
            <FiX size={20} />
          </button>
        </header>

        {cert.certImage ? (
          <div className={styles.imageWrap}>
            <Image
              src={cert.certImage}
              alt={cert.title}
              width={1200}
              height={1600}
              className={styles.image}
              quality={95}
            />
          </div>
        ) : (
          <p className={styles.noImage}>{cert.desc}</p>
        )}

        <footer className={styles.footer}>
          {cert.link && cert.link.startsWith('http') && (
            <a href={cert.link} target="_blank" rel="noopener noreferrer" className={styles.verifyBtn}>
              Verify credential <FiExternalLink />
            </a>
          )}
        </footer>
      </div>
    </div>
  )
}
