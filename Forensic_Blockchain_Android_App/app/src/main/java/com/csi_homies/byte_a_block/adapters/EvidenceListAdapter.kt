package com.csi_homies.byte_a_block.adapters

import android.content.Context
import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.RecyclerView
import com.csi_homies.byte_a_block.activities.EvidenceInfoActivity
import com.csi_homies.byte_a_block.activities.MainActivity
import com.csi_homies.byte_a_block.activities.R
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicEvidenceInfo
import com.csi_homies.byte_a_block.utils.Constants
import com.google.gson.Gson

class EvidenceListAdapter (private val list: ArrayList<BasicEvidenceInfo>, private val context: Context,
                           private val case_id: Int, private val case_name: String) :
    RecyclerView.Adapter<EvidenceListAdapter.ViewHolder>(){

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.evidence_list_row, parent, false)

        return ViewHolder(view, context, list)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bindViews(list[position])
    }

    override fun getItemCount(): Int {
        return list.size
    }

    inner class ViewHolder(itemView: View, context: Context, list:ArrayList<BasicEvidenceInfo>): RecyclerView.ViewHolder(itemView), View.OnClickListener{
        var mContext = context

        var evidenceNumber = itemView.findViewById(R.id.evidenceListNumberText) as TextView
        var evidenceSerialNo = itemView.findViewById(R.id.evidenceListSerialNoText) as TextView
        var evidenceLogBy = itemView.findViewById(R.id.evidenceListLogByText) as TextView

        var evidenceStatusIcon = itemView.findViewById(R.id.evidenceListStatusImage) as ImageView
        var evidenceStatus = itemView.findViewById(R.id.evidenceListStatusText) as TextView

        var evidenceList = itemView.findViewById(R.id.evidenceCardView) as CardView

        fun bindViews(basicEvidenceInfo: BasicEvidenceInfo) {
            evidenceNumber.text = "Evidence ${basicEvidenceInfo.evid_id.toString()}"
            evidenceSerialNo.text = basicEvidenceInfo.serial_no
            evidenceLogBy.text = "Logged by: ${basicEvidenceInfo.handler.toString()}"

            when (basicEvidenceInfo.curr_status) {
                "In Transit" -> evidenceStatusIcon.setBackgroundResource(R.drawable.ic_in_transit)
                "Check Into Storage" -> evidenceStatusIcon.setBackgroundResource(R.drawable.ic_checked_in)
                "Check Out of Storage" -> evidenceStatusIcon.setBackgroundResource(R.drawable.ic_checked_out)
                "Analysis" -> evidenceStatusIcon.setBackgroundResource(R.drawable.outline_plagiarism_black_48)
                "Drive Cloning" -> evidenceStatusIcon.setBackgroundResource(R.drawable.outline_content_copy_black_48)
                "Court Appearance" -> evidenceStatusIcon.setBackgroundResource(R.drawable.outline_gavel_black_48)
            }

            evidenceStatus.text = basicEvidenceInfo.curr_status

            evidenceList.setOnClickListener(this)
        }

        override fun onClick(v: View?) {
            // Gets the view holder's position, its a free method
            var mPosition: Int = adapterPosition

            when(v!!.id){
                evidenceList.id -> {
//                    mContext.startActivity(Intent(mContext, EvidenceInfoActivity::class.java))
                    val i = Intent(mContext, EvidenceInfoActivity::class.java)
                    i.putExtra(Constants.SELECTED_CASE_ID_ID, case_id)
                    i.putExtra(Constants.SELECTED_CASE_NAME_ID, case_name)
                    i.putExtra(Constants.SELECTED_EVIDENCE_ID_ID, list[mPosition].evid_id)
                    mContext.startActivity(i)
                }
            }
        }

    }

}