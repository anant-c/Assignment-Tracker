"use client";


import { motion } from "motion/react";
import {Spotlight} from "./ui/spotlight-new"
import { BackgroundGradient } from "./ui/background-gradient";
import { Button } from "./ui/button"
import { FlipWords } from "./ui/flip-words";
import { useNavigate } from "react-router-dom";

export default function HeroSectionOne() {
  const navigate = useNavigate();
  const words = ["posting", "tracking", "submitting", "evaluating"];
  return (
    <div className="relative flex flex-col items-center justify-center min-w-screen">
      <Navbar />
      <Spotlight
      />
      <div className="absolute inset-y-0 z-10 left-0 h-full w-px bg-neutral-200/80 dark:bg-neutral-800/80">
        <div className="absolute top-0 h-40 w-px bg-gradient-to-b from-transparent via-blue-500 to-transparent" />
      </div>
      <div className="absolute inset-y-0 right-0 h-full w-px bg-neutral-200/80 dark:bg-neutral-800/80">
        <div className="absolute h-40 w-px bg-gradient-to-b from-transparent via-blue-500 to-transparent" />
      </div>
      <div className="absolute inset-x-0 bottom-0 h-px w-full bg-neutral-200/80 dark:bg-neutral-800/80">
        <div className="absolute mx-auto h-px w-40 bg-gradient-to-r from-transparent via-blue-500 to-transparent" />
      </div>
      <div className=" flex flex-col px-4 py-10 md:py-20 items-center">
        <div className="flex justify-center items-center gap-2 border-1 border-gray-800 rounded-full w-35 p-2 mb-6">
          <div className="w-2 h-2 rounded-full bg-green-600 animate-pulse"></div>
          Version 1.0
        </div>
        <h1 className="relative z-10 mx-auto max-w-4xl text-center text-2xl font-bold text-slate-700 md:text-4xl lg:text-7xl dark:text-slate-300">
          {"Create. Submit. Track."
            .split(" ")
            .map((word, index) => (
              <motion.span
                key={index}
                initial={{ opacity: 0, filter: "blur(4px)", y: 10 }}
                animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
                transition={{
                  duration: 0.3,
                  delay: index * 0.1,
                  ease: "easeInOut",
                }}
                className="mr-2 inline-block"
              >
                {word}
              </motion.span>
            ))}
        </h1>
        <motion.p
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          transition={{
            duration: 0.3,
            delay: 0.8,
          }}
          className="relative z-10 mx-auto max-w-xl py-4 text-center text-lg font-normal text-neutral-600 dark:text-neutral-400"
        >
          With our modern platform, teachers can post assignments and students can submit them in minutes. Experience seamless, smart, and efficient classroom collaboration—anytime, anywhere.
        </motion.p>
        <motion.div
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          transition={{
            duration: 0.3,
            delay: 1,
          }}
          className="relative z-10 mt-8 flex flex-wrap items-center justify-center gap-4"
        >
          <button className="w-60 transform rounded-lg cursor-pointer bg-black px-6 py-2 font-medium text-white transition-all duration-300 hover:-translate-y-0.5 hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200">
            Get Started
          </button>
          <button className="w-60 transform rounded-lg cursor-pointer border border-gray-300 bg-white px-6 py-2 font-medium text-black transition-all duration-300 hover:-translate-y-0.5 hover:bg-gray-100 dark:border-gray-700 dark:bg-black dark:text-white dark:hover:bg-gray-900">
            What's More?
          </button>
        </motion.div>
          <div className="h-[15rem] flex justify-center text-center items-center px-4">
            <div className="text-4xl mx-auto font-normal text-neutral-600 dark:text-neutral-400">
              Your smart companion for 
              <FlipWords words={words} />
              assignments
            </div>
          </div>
          <div className="grid grid-cols-1 m-10 gap-10 lg:grid-cols-2 lg:gap-30">
          <BackgroundGradient className="flex flex-col items-center rounded-[22px] max-w-sm p-4 sm:p-10 bg-white dark:bg-zinc-900">
            <img
              src={`https://cdn-icons-png.flaticon.com/512/3534/3534172.png`}
              alt="student"
              className="object-contain w-[200px] h-[200px] lg:h-[400px] lg:w-[400px]"
            />
            <p className="text-base text-center sm:text-3xl text-black mt-4 mb-2 dark:text-neutral-200">
              Student
            </p>
    
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Browse assignments, complete your work, and submit before the deadline — all in one place. Once graded, get instant feedback and view your results seamlessly.
            </p>
            <Button onClick={() => navigate('/login/student')} className="mt-4 py-2 px-4 text-md lg:text-lg cursor-pointer" variant="default" size="md">Log In</Button>
          </BackgroundGradient>
          <BackgroundGradient className="flex flex-col items-center rounded-[22px] max-w-sm p-4 sm:p-10 bg-white dark:bg-zinc-900">
            <img
              src={`https://cdn-icons-png.flaticon.com/512/10559/10559204.png`}
              alt="teacher"
              className="object-contain w-[200px] h-[200px] lg:h-[400px] lg:w-[400px]"
            />
            <p className="text-base text-center sm:text-3xl text-black mt-4 mb-2 dark:text-neutral-200">
              Teacher
            </p>
          
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Create and manage assignments effortlessly. Set deadlines, track student submissions, and provide grades and feedback with ease — all from a single dashboard.
            </p>
            <Button onClick={() => navigate('/login/teacher')} className="mt-4 py-2 px-4 text-md lg:text-lg cursor-pointer" variant="default" size="md">Log In</Button>
          </BackgroundGradient>
        </div>
      </div>
    </div>
  );
}

const Navbar = () => {
  return (
    <nav className="flex w-full items-center justify-between border-t border-b border-neutral-200 px-4 py-4 dark:border-neutral-800">
      <div className="flex items-center gap-2">
        <div className="size-7 rounded-full bg-gradient-to-br from-violet-500 to-pink-500" />
        <h1 className="text-base font-bold md:text-2xl">AssignMate</h1>
      </div>
      <button className="w-24 cursor-pointer transform rounded-lg bg-black px-6 py-2 font-medium text-white transition-all duration-300 hover:-translate-y-0.5 hover:bg-gray-800 md:w-32 dark:bg-white dark:text-black dark:hover:bg-gray-200">
        Login
      </button>
    </nav>
  );
};
