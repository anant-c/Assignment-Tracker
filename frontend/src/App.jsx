import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {Button} from '@/components/ui/button'
import HeroSectionOne from './components/hero-section-demo-1'
import { Routes, Route, useNavigate } from 'react-router-dom'
import LogIn from './pages/LogIn.jsx'

function App() {

  useEffect(() => {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  return (
    <div className='max-w-screen min-h-screen overflow-x-hidden'>
      <Routes>
        <Route path="/" element={<HeroSectionOne />} />
        <Route path="/login/student" element={<LogIn role="student" />} />
        <Route path="/login/teacher" element={<LogIn role="teacher" />} />
      </Routes>

    </div>
      
  
  )
}

export default App
