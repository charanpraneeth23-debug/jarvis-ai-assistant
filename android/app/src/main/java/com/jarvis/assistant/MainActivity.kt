package com.jarvis.assistant

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.jarvis.assistant.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.askButton.setOnClickListener {
            val userInput = binding.commandInput.text.toString().trim()

            if (userInput.isEmpty()) {
                binding.responseText.text = "Please type a command first."
                return@setOnClickListener
            }

            binding.responseText.text = "Jarvis heard: $userInput\n\nI am ready to connect to your AI backend and system actions."
        }
    }
}
