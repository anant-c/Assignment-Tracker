import React from 'react';

export default function TeacherLogin() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-300 via-yellow-200 to-orange-300 dark:from-zinc-800 dark:via-zinc-900 dark:to-black">
      <div className="w-full max-w-md px-8 py-10 bg-white bg-opacity-90 dark:bg-zinc-800 dark:bg-opacity-90 backdrop-blur-xl rounded-3xl shadow-2xl">
        <div className="flex justify-center mb-4">
          <div className="text-5xl text-pink-600 dark:text-white">👩‍🏫</div>
        </div>
        <h2 className="text-3xl font-bold text-center text-gray-800 dark:text-white mb-6">
          Teacher Login
        </h2>
        <form>
          <input
            type="text"
            placeholder="Full Name"
            className="w-full mb-4 p-3 rounded-xl border border-gray-300 dark:border-gray-700 dark:bg-zinc-900 dark:text-white focus:ring-2 focus:ring-pink-300"
          />
          <input
            type="email"
            placeholder="Email"
            className="w-full mb-4 p-3 rounded-xl border border-gray-300 dark:border-gray-700 dark:bg-zinc-900 dark:text-white focus:ring-2 focus:ring-pink-300"
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full mb-6 p-3 rounded-xl border border-gray-300 dark:border-gray-700 dark:bg-zinc-900 dark:text-white focus:ring-2 focus:ring-pink-300"
          />
          <button
            type="submit"
            className="w-full p-3 text-lg font-semibold text-white rounded-xl shadow-md transition-all bg-gradient-to-r from-pink-500 via-yellow-500 to-orange-500 hover:brightness-110"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
