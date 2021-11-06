package com.csi_homies.byte_a_block.activities

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.csi_homies.byte_a_block.adapters.EvidenceListAdapter
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicEvidenceInfo
import com.csi_homies.byte_a_block.models.basic_case_info_response.Case
import com.csi_homies.byte_a_block.utils.Constants
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_case_info.*
import java.util.*

private lateinit var currentCaseInfo: Case

class CaseInfoActivity : BaseActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_case_info)

        currentCaseInfo = Gson().fromJson(intent.getStringExtra(Constants.SELECTED_CASE_INFO_ID), Case::class.java)

        setupCaseInfoUI(currentCaseInfo)
    }

    private fun setupCaseInfoUI(case: Case) {
        setupActionBar(case.case_name)

        currentCaseLocationText.text = case.location
        currentCaseDateText.text = getDateString(case.date.toLong())
        currentCaseStatusText.text = case.case_status

        setUpEvidenceRecyclerView(case)
    }

    // RecyclerView necessities
    private var basicEvidenceListItems: ArrayList<BasicEvidenceInfo>? = null
    private var adapter:EvidenceListAdapter? = null
    private var layoutManager: RecyclerView.LayoutManager? = null

    private fun setUpEvidenceRecyclerView(case: Case) {
        basicEvidenceListItems = ArrayList<BasicEvidenceInfo>()
        layoutManager = LinearLayoutManager(this)

        basicEvidenceListItems = ArrayList(case.evidence)

        adapter = EvidenceListAdapter(basicEvidenceListItems!!, this, case.case_id, case.case_name)

        if (case.evidence.isNotEmpty()){
            evidenceRecyclerView.visibility = View.VISIBLE
            noEvidenceText.visibility = View.GONE

            evidenceRecyclerView.layoutManager = layoutManager
            evidenceRecyclerView.adapter = adapter
        }
    }

    private fun setupActionBar(caseIDTitle: String) {
        var actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.title = "Case $caseIDTitle"
            actionBar.setHomeAsUpIndicator(R.drawable.ic_white_color_back_24dp)
            actionBar.setDisplayHomeAsUpEnabled(true)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return super.onSupportNavigateUp()
    }

    override fun onBackPressed() {
        val openMainActivity = Intent(this@CaseInfoActivity, MainActivity::class.java)
        openMainActivity.flags = Intent.FLAG_ACTIVITY_REORDER_TO_FRONT
        startActivityIfNeeded(openMainActivity, 0)
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.add_new_evid_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == R.id.newEvidMenuButton) {
            val i = Intent(this@CaseInfoActivity, PhotographingEvidenceActivity::class.java)
            i.putExtra(Constants.START_PHOTO_TAKING_ACTIVITY_ID, Constants.ADD_NEW_EVIDENCE)
            i.putExtra(Constants.SELECTED_CASE_NAME_ID, currentCaseInfo.case_name)
            i.putExtra(Constants.SELECTED_CASE_ID_ID, currentCaseInfo.case_id)
            startActivity(i)
        }
        return super.onOptionsItemSelected(item)
    }
}