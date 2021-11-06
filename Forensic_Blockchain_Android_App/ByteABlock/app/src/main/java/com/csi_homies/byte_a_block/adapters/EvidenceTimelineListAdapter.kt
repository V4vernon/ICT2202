package com.csi_homies.byte_a_block.adapters

import android.annotation.SuppressLint
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.csi_homies.byte_a_block.activities.BaseActivity
import com.csi_homies.byte_a_block.activities.R
import com.csi_homies.byte_a_block.models.evidence_info_response.EvidenceHistory
import java.text.SimpleDateFormat
import java.util.*
import kotlin.collections.ArrayList

class EvidenceTimelineListAdapter (private val list: ArrayList<EvidenceHistory>, private val context: Context) :
    RecyclerView.Adapter<EvidenceTimelineListAdapter.ViewHolder>(){

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.evidence_timeline_row, parent, false)

        return ViewHolder(view, list)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bindViews(list[position], position)
    }

    override fun getItemCount(): Int {
        return list.size
    }

    inner class ViewHolder(itemView: View, list: ArrayList<EvidenceHistory>): RecyclerView.ViewHolder(itemView){

        var timelineDate = itemView.findViewById(R.id.timelineDateText) as TextView
        var timelineDescription = itemView.findViewById(R.id.timelineDescriptionText) as TextView

        var topLine = itemView.findViewById(R.id.timelineTopLine) as View
        var bottomLine = itemView.findViewById(R.id.timelineBottomLine) as View

        @SuppressLint("SetTextI18n")
        fun bindViews(evidenceHistory: EvidenceHistory, position: Int) {
            timelineDate.text = getDateString(evidenceHistory.date.toLong())
            timelineDescription.text = "Status: ${evidenceHistory.status.toString()}\n" +
                    "Purpose: ${evidenceHistory.purpose.toString()}\n" +
                    "By: ${evidenceHistory.handler.toString()}"

            if (list.size == 1) {
                topLine.visibility = View.INVISIBLE
                bottomLine.visibility = View.INVISIBLE
            } else {
                if (position == 0){
                    topLine.visibility = View.INVISIBLE
                } else if (position == (list.size - 1)){
                    bottomLine.visibility = View.INVISIBLE
                }
            }
        }
    }

    // Displaying epoch time in human readable format
    val simpleDateFormat = SimpleDateFormat("dd MMM yy\nHH:mm", Locale.ENGLISH)
    fun getDateString(time: Long) : String = simpleDateFormat.format(time * 1000L)
}