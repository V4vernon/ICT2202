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
import com.csi_homies.byte_a_block.utils.Constants
import com.csi_homies.byte_a_block.activities.CaseInfoActivity
import com.csi_homies.byte_a_block.activities.R
import com.csi_homies.byte_a_block.models.basic_case_info_response.Case
import com.google.gson.Gson

class CaseListAdapter (private val list: ArrayList<Case>, private val context: Context) :
    RecyclerView.Adapter<CaseListAdapter.ViewHolder>(){

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.case_list_row, parent, false)

        return ViewHolder(view, context, list)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bindViews(list[position])
    }

    override fun getItemCount(): Int {
        return list.size
    }

    inner class ViewHolder(itemView: View, context: Context, list:ArrayList<Case>): RecyclerView.ViewHolder(itemView), View.OnClickListener {
        var mContext = context

        var caseNumber = itemView.findViewById(R.id.caseListCaseNameText) as TextView
        var caseLocation = itemView.findViewById(R.id.caseListLocationText) as TextView

        var caseStatusIcon = itemView.findViewById(R.id.caseListCaseStatusImage) as ImageView
        var caseStatusText = itemView.findViewById(R.id.caseListCaseStatusText) as TextView

        var caseList = itemView.findViewById(R.id.caseCardView) as CardView

        fun bindViews(case: Case) {
            caseNumber.text = case.case_name
            caseLocation.text = case.location
            caseStatusText.text = case.case_status

            caseList.setOnClickListener(this)

            if (case.case_status == "Completed")
                caseStatusIcon.setBackgroundResource(R.drawable.ic_case_completed)
            else
                caseStatusIcon.setBackgroundResource(R.drawable.ic_case_in_progress)

        }

        override fun onClick(v: View?) {
            // Gets the view holder's position, its a free method
            var mPosition: Int = adapterPosition

            when(v!!.id){
                caseList.id -> {
                    val populateCaseInfoActivityIntent = Intent(mContext, CaseInfoActivity::class.java)
                    populateCaseInfoActivityIntent.putExtra(Constants.SELECTED_CASE_INFO_ID, Gson().toJson(list[mPosition]))
                    mContext.startActivity(populateCaseInfoActivityIntent)
                }
            }
        }
    }

}