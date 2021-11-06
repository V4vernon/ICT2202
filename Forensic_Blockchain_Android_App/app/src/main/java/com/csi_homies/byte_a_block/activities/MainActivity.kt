package com.csi_homies.byte_a_block.activities

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import com.csi_homies.byte_a_block.utils.Constants
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : BaseActivity() {

    val case_info: BasicCaseInfoResponse? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val case_info = intent.getStringExtra(Constants.CASE_INFO_ID)

        showProgressDialog("Loading Case Data...")
        if (case_info == null)
            // Only occurs when user is loading into this activity
            loadCasesInMainActivity(getUsername(), getPassword(), this@MainActivity)
         else
            // Only occurs when coming from sign in activity
            setupCaseUI(Gson().fromJson(case_info, BasicCaseInfoResponse::class.java), this)
        hideProgressDialog()

        caseSwipeRefreshLayout!!.setOnRefreshListener {
            loadCasesInMainActivity(getUsername(), getPassword(), this@MainActivity)
            caseSwipeRefreshLayout!!.isRefreshing = false
        }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.main_top_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == R.id.logOutMenuButton) {
            clearStoredUserNameAndPassword()
            finish()
            startActivity(Intent(this, IntroActivity::class.java))
        }
        return super.onOptionsItemSelected(item)
    }
}