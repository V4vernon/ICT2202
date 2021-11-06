package com.csi_homies.byte_a_block.activities

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import com.csi_homies.byte_a_block.models.evidence_info_response.EvidenceInfoResponse
import com.csi_homies.byte_a_block.network.BasicCaseInfoGet
import com.csi_homies.byte_a_block.network.EvidenceInfoGet
import com.csi_homies.byte_a_block.utils.Constants
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_evidence_info.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import android.graphics.BitmapFactory

import android.graphics.Bitmap
import android.util.Base64
import android.view.Menu
import android.view.MenuItem
import android.view.View
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.csi_homies.byte_a_block.adapters.EvidenceListAdapter
import com.csi_homies.byte_a_block.adapters.EvidenceTimelineListAdapter
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicEvidenceInfo
import com.csi_homies.byte_a_block.models.basic_case_info_response.Case
import com.csi_homies.byte_a_block.models.evidence_info_response.EvidenceHistory
import kotlinx.android.synthetic.main.activity_case_info.*
import java.util.ArrayList


class EvidenceInfoActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_evidence_info)

        val selectedCaseId = intent.getIntExtra(Constants.SELECTED_CASE_ID_ID, 1)
        val selectedEvidenceId = intent.getIntExtra(Constants.SELECTED_EVIDENCE_ID_ID, 1)
        val selectedCaseName = intent.getStringExtra(Constants.SELECTED_CASE_NAME_ID)

        setupActionBar(selectedCaseName!!, selectedEvidenceId)

        getEvidenceInfo(selectedCaseId, selectedEvidenceId)

    }

    private fun getEvidenceInfo(case_id: Int, evid_id: Int){
        if (isNetworkAvailable(this@EvidenceInfoActivity)) {
            val retrofit: Retrofit = Retrofit.Builder()
                .baseUrl(Constants.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

            val service: EvidenceInfoGet = retrofit.create<EvidenceInfoGet>(EvidenceInfoGet::class.java)

            val listCall: Call<EvidenceInfoResponse> = service.getEvidenceInfo(case_id.toString(), evid_id.toString())

            showProgressDialog("Retrieving Evidence Information...")

            listCall.enqueue(object: Callback<EvidenceInfoResponse> {
                override fun onResponse(
                    call: Call<EvidenceInfoResponse>,
                    response: Response<EvidenceInfoResponse>
                ) {
                    if (response.isSuccessful){
                        val evidenceInfoResponse: EvidenceInfoResponse? = response.body()
                        if (evidenceInfoResponse != null) {
                            evidenceInfoSerialNoText.text = evidenceInfoResponse.serial_no.toString()
                            evidenceInfoLogByText.text = evidenceInfoResponse.handler.toString()
                            evidenceInfoEvidenceTypeText.text = evidenceInfoResponse.evid_type.toString()
                            evidenceInfoLocationText.text = evidenceInfoResponse.location.toString()
                            evidenceInfoCurrentStatusText.text = evidenceInfoResponse.curr_status.toString()
                            evidenceInfoNotesText.text = evidenceInfoResponse.notes.toString()

                            if (evidenceInfoResponse.image.toString() != "corrupted") {
                                val decodedString: ByteArray = Base64.decode(evidenceInfoResponse.image, Base64.DEFAULT)
                                val decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size)
                                latestEvidenceImage.setImageBitmap(decodedByte)
                            }

                            setUpEvidenceTimelineRecyclerView(evidenceInfoResponse.evidence_history)
                        }
                        hideProgressDialog()
                    } else {
                        when(response.code()) {
                            400 -> showErrorSnackBar("Error 400, Bad Request!")
                            404 -> showErrorSnackBar("Error 404, Page is not found!")
                            else -> showErrorSnackBar("Generic Error!")
                        }
                        hideProgressDialog()
                    }
                }

                override fun onFailure(call: Call<EvidenceInfoResponse>, t: Throwable) {
                    showErrorSnackBar("Network Exception occurred! ${t.toString()}")

                    hideProgressDialog()
                }

            })
        }
    }

    // RecyclerView necessities
    private var evidenceTimeLineListItems: ArrayList<EvidenceHistory>? = null
    private var adapter: EvidenceTimelineListAdapter? = null
    private var layoutManager: RecyclerView.LayoutManager? = null

    private fun setUpEvidenceTimelineRecyclerView(evidenceHistory: List<EvidenceHistory>) {
        evidenceTimeLineListItems = ArrayList<EvidenceHistory>()
        layoutManager = LinearLayoutManager(this)

        evidenceTimeLineListItems = ArrayList(evidenceHistory.asReversed())

        adapter = EvidenceTimelineListAdapter(evidenceTimeLineListItems!!, this@EvidenceInfoActivity)

        evidenceTimeLineRecyclerView.layoutManager = layoutManager
        evidenceTimeLineRecyclerView.adapter = adapter
    }

    private fun setupActionBar(caseName: String, evidId: Int) {
        var actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.title = "Case $caseName Evidence ${evidId.toString()}"
            actionBar.setHomeAsUpIndicator(R.drawable.ic_white_color_back_24dp)
            actionBar.setDisplayHomeAsUpEnabled(true)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        val openMainActivity = Intent(this@EvidenceInfoActivity, CaseInfoActivity::class.java)
        openMainActivity.flags = Intent.FLAG_ACTIVITY_REORDER_TO_FRONT
        startActivityIfNeeded(openMainActivity, 0)
        return super.onSupportNavigateUp()
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.modify_evid_status_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == R.id.startModifyEvidActivityButton) {
            val i = Intent(this@EvidenceInfoActivity, PhotographingEvidenceActivity::class.java)
            i.putExtra(Constants.START_PHOTO_TAKING_ACTIVITY_ID, Constants.MODIFY_EVIDENCE_STATUS)
            i.putExtra(Constants.SELECTED_CASE_ID_ID, intent.getIntExtra(Constants.SELECTED_CASE_ID_ID, 0))
            i.putExtra(Constants.SELECTED_EVIDENCE_ID_ID, intent.getIntExtra(Constants.SELECTED_EVIDENCE_ID_ID, 0))
            startActivity(i)
        }
        return super.onOptionsItemSelected(item)
    }
}