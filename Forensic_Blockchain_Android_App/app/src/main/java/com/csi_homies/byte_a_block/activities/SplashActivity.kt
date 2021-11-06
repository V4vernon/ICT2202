package com.csi_homies.byte_a_block.activities

import android.content.Intent
import android.graphics.Typeface
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.view.WindowInsets
import android.view.WindowManager
import kotlinx.android.synthetic.main.activity_splash.*

class SplashActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        // FLAG_FULLSCREEN got deprecated after R
        @Suppress("DEPRECATION")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            window.insetsController?.hide(WindowInsets.Type.statusBars())
        } else {
            window.setFlags(
                WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN
            )
        }

        // To use the font asset that is free for commercial use
        val typeFace: Typeface = Typeface.createFromAsset(assets, "carbon bl.ttf")
        appNameTextView.typeface = typeFace

        // Launch screen page before loading into the app
        Handler().postDelayed({
            if (isUserSignedIn())
                startActivity(Intent(this@SplashActivity, MainActivity::class.java))
            else
                startActivity(Intent(this@SplashActivity, IntroActivity::class.java))
            finish()
        }, 1000)
    }
}